import ast
import asyncio
import json

import dspy

from backend.app.core.config import settings
from backend.app.services.ai_service.dspy_signatures import GenerateGraphs
from backend.app.services.ai_service.response_models import GraphResponse
from backend.app.services.scraping_service.jina_scraper import jina_scrape
from backend.app.utils.language_enum import Language


class ArticleGenerator:

    def __init__(self) -> None:
        self.api_key = settings.LITE_LLM_KEY
        self.litellm_url = "http://147.175.151.44/"
        self.models = {
            "gpt-4.1-mini": "openai/gpt-4.1-mini",
            "o3-mini": "openai/o3-mini",
        }

    def _configure_lm(self, model_name: str) -> None:
        kwargs = {
            "model": model_name,
            "api_key": self.api_key,
            "base_url": self.litellm_url,
        }
        if model_name.startswith("openai/o3-"):
            kwargs["temperature"] = 1.0
            kwargs["max_tokens"] = 5000

        lm = dspy.LM(**kwargs)
        dspy.settings.configure(lm=lm, async_max_workers=8)

    async def generate_graph(
        self,
        scraped_content: str | None,
        language: Language = Language.SLOVAK,
    ) -> GraphResponse:
        self._configure_lm(self.models.get("gpt-4.1-mini"))

        generator = GenerateGraphs

        generate_graphs_program = dspy.asyncify(generator())
        kwargs = {
            "scraped_content": scraped_content,
            "language": language,
        }

        graph_response = await generate_graphs_program(**kwargs)

        graph_data = graph_response.graph_data
        if isinstance(graph_data, str):
            graph_data = json.loads(graph_data)

        graph_axis_labels = graph_response.graph_axis_labels
        if isinstance(graph_axis_labels, str):
            graph_axis_labels = json.loads(graph_axis_labels)

        return GraphResponse(
            gen_graph=graph_response.gen_graph,
            graph_title=graph_response.graph_title,
            graph_type=graph_response.graph_type,
            graph_axis_labels=graph_axis_labels,
            graph_data=graph_data,
        )


def clean_graph_data(graph_metadata: GraphResponse) -> GraphResponse:
    if not (graph_metadata.gen_graph and graph_metadata.graph_data):
        return

    graph_labels_key = "x_vals" if graph_metadata.graph_type == "scatter" else "labels"
    graph_values_key = "y_vals" if graph_metadata.graph_type == "scatter" else "values"

    labels = graph_metadata.graph_data.get(graph_labels_key, [])
    values = graph_metadata.graph_data.get(graph_values_key, [])

    """print('BEFORE PARSING:')
    print('LABELS:', labels,)
    print('VALUES:', values, '\n')"""

    # Attempt to parse labels and values if they are strings and not individual elements in a list
    if isinstance(labels, list) and all(isinstance(item, str) for item in labels):
        try:
            labels = ast.literal_eval(f"[{labels[0]}]") if len(labels) == 1 else labels
        except (ValueError, SyntaxError):
            labels = []

    if isinstance(values, list) and all(isinstance(item, str) for item in values):
        try:
            values = ast.literal_eval(f"[{values[0]}]") if len(values) == 1 else values
        except (ValueError, SyntaxError):
            values = []

    """print('AFTER PARSING:')
    print('LABELS:', labels)
    print('VALUES:', values, '\n')"""

    # Need to also filter labels and values, sometimes it has none values and therefore it is necessary to also
    # remove corresponding element from the other dict to prevent mismatch, except for histogram, which has labels = None
    if graph_metadata.graph_type != "histogram":
        filtered_labels = []
        filtered_values = []
        for label, value in zip(labels, values):
            if value is not None:
                filtered_labels.append(label)
                filtered_values.append(value)

        # Check if after filtering it, still has enough datapoints to create a graph
        if len(filtered_labels) >= 2:
            graph_metadata.graph_data[graph_labels_key] = filtered_labels
            graph_metadata.graph_data[graph_values_key] = filtered_values
        else:
            # If not enough valid points, disable graph
            graph_metadata.gen_graph = False
            graph_metadata.graph_data = None

    return graph_metadata


async def main() -> None:
    lm = ArticleGenerator()

    url = "https://susr.statistics.sk/wps/portal/ext/products/informationmessages/inf_sprava_detail/08f3b8fa-9fc3-41a6-af17-878dd2ad738d/!ut/p/z1/rVddk6JKDP0t--AjkqaBbu8boCKKjogwM7zcYhRHrh_MKqvr_PrbOrNWCWt6tmrxQaycpJOTpGPURH1Sk216yF_TMi-26Vr8fk7MfwPmcdsmFoDtU_D6g3DUc7qaGxlqrCZqMtuWb-VSfS5e9ulS2a-UfLtQ0lXZAPFS7DbC2mGbKfu3XXo4NeCwz8qV-Aa-oC98kSqtxYwqOklNJV0QpnDG53MtnTPK52fzb7N8rj5_Cf148Tf2xx_-PkShDpbBiNYajzXX1NTkvphbxqe-41o9nfnCQd81wLN60aQVUAoWvegjdHzow53Hgq_pXx102ZSANxqFUcwD2ukat_7fiiNd-9S_HuD2Ii4ANrhuyyc6hUr8E9KFAGAwGvCpN2wzib6tY-c_OESmb6L6PVrV53asgcdGEzIIAncQMcz_wKn5zw0G4oAwAohDAL_Cf0U80av8QzhsgReH-vSBM40Scnv-rbjvsVr9mURkfWL4hu2b1_q5JzZx_92gVeGPx7wt4h9C3-1w6o41mT7D9GFCJPq9qv9hZAnxxDMc36YPliHhr1epP049AyyvDR1K-9DtgOx8DfVf0_H-iUDD6icCgtcfsVmlfm7FsZR_A81fv-Z_HZBg9Er6b6ADlj_Xr-WvDkDON671hwCw-nF0_Pwz4Ja_3lCkt-uP43FnSiYx1PirAf6M_zrBX7q_EMBZ3wqCIPTjGNxY64JHiQujSJTI1PzURwBfmh8IIMHH0-N53komoMxGgg3ZywyWZfED0A3HmtXSXac9eRAsTB2Nh76pgWjTBMtD0NIkFlwTt3AZtChg9MtJbNRWLouB4wiAMW0b8YiOO7rEgq1XfahWo4YDLu2GWiBE5oNZi6I-kbFsMjBqFup3OgawpriFj6ku66sEHbzXqsYGLw5gsjApTjU4uAUQgcrqAXALjq7jVX2ZjxhgSKkEMNXxgrmMUJxJQ9I4fq39b6cE78osWDImiayiRF8ItvuybUJsT_l_378nlliRim2Z_SzVp187UgP2pdiLZspFshW7UpltTueNaZ6v0rLY3bwrq0O6zsuT8p4fijJtwI9V-l4c0jJbZ-qzuPTZ3UufiH-Vhzw7qtH2vIqt1fAPd6q-bOiIMLXd0Bm-CrNpuTxvf4X69CXbGEN_c4sUMeQvm-ZxtmlCk3EGlDGua3rLNERNCy-s7QvlIoBdtsh22a75YyeW32VZvu3_aUADjsdj87UoXtdZc1ZsGvA7lWWxF97fItW3zYbTU448ymrSufPpHU_03R4pyYv49rNH69u3_wFiRv36/dz/d5/L0lDUmlTUSEhL3dHa0FKRnNBLzROV3FpQSEhL3Nr/"

    scraped_content = await jina_scrape(url)
    graph_response = await lm.generate_graph(scraped_content, language=Language.SLOVAK)

    print("GRAPH BEFORE CLEAN:\n", graph_response, "\n")
    cleaned_graph = clean_graph_data(graph_response)
    print("GRAPH AFTER CLEAN:\n", cleaned_graph, "\n")


if __name__ == "__main__":
    asyncio.run(main())

    """graph_response = GraphResponse(
        chain_of_thought=None,
        gen_graph=True,
        graph_title='Medziročný rast HDP Slovenska 2021-2024 po jarnej revízii',
        graph_type='bar',
        graph_axis_labels={'x_axis': 'Rok', 'y_axis': 'Medziročná zmena HDP (%)'},
        graph_data={'labels': ['2021', '2022', '2023', '2024'], 'values': ['None, None, 2.2, 2.1']}
    )

    clean = clean_graph_data(graph_response)
    print('CLEANED GRAPH:\n', clean)"""

# region TEST CLANKY
# CLANKY NA TEST
# z tohto mi spravil pie chart
"""https://slovak.statistics.sk/wps/portal/ext/products/informationmessages/inf_sprava_detail/f6869351-8ff8-41d7-ae37-06eaa23a88e2/!ut/p/z1/rZNLc5swFIX_SrrwUqOLxENeYk-CcWxPwcGxtenIGGyCDcSoJOTXR8TTaTtTHouyEYzuPTo69wNzvMU8E1VyFDLJM3FW3ztu_vAsl00mmg0wWVBw54_r1Wz6QJzAwM9_F7CVfw_uk_3d8ee6BrqBudq2Pc9bLzYbcDbkAVyqObAKAqVm4g3mmIeZLOQJ7_J9KU6oTFGSxUikcgTqJb9elJsqi1BZXEVVj6AqI5mqNTaZOaaGhlgcM6RrBwuJiFoIzEgIQgVjEWnkizA54N2g6tt1OvzyIXFMHXumWwsAtnAMcO1Z4I89SsGmfXHc-qHlsWFYf4dB3i3_3OTVc4M-Dd5p8snE6zLFO2XUai3yVZJVEr3hIGvGf8br33M0YkOjRAcUHyIT6XpI0JgIhiwj3ocENEpDA88Az_uyUmyT63K6PCplIU8NdDnepkKKc368-4O8OjzdfbHXtCQvr6_cVszmmYzeJd7-gnYEpVTlIfrayRS8xTU__Exl3YJx50m3fNoGqVnt-QzifN4H8r_DGaTdFdL__LOLS3BhtE6SBKU-W95Tne9r-jFZIbW-2d8-Ab6TVrk!/dz/d5/L2dBISEvZ0FBIS9nQSEh/"""

# mixnute data problem (percenta a miliardy)
"""https://susr.statistics.sk/wps/portal/ext/products/informationmessages/inf_sprava_detail/08f3b8fa-9fc3-41a6-af17-878dd2ad738d/!ut/p/z1/rVddk6JKDP0t--AjkqaBbu8boCKKjogwM7zcYhRHrh_MKqvr_PrbOrNWCWt6tmrxQaycpJOTpGPURH1Sk216yF_TMi-26Vr8fk7MfwPmcdsmFoDtU_D6g3DUc7qaGxlqrCZqMtuWb-VSfS5e9ulS2a-UfLtQ0lXZAPFS7DbC2mGbKfu3XXo4NeCwz8qV-Aa-oC98kSqtxYwqOklNJV0QpnDG53MtnTPK52fzb7N8rj5_Cf148Tf2xx_-PkShDpbBiNYajzXX1NTkvphbxqe-41o9nfnCQd81wLN60aQVUAoWvegjdHzow53Hgq_pXx102ZSANxqFUcwD2ukat_7fiiNd-9S_HuD2Ii4ANrhuyyc6hUr8E9KFAGAwGvCpN2wzib6tY-c_OESmb6L6PVrV53asgcdGEzIIAncQMcz_wKn5zw0G4oAwAohDAL_Cf0U80av8QzhsgReH-vSBM40Scnv-rbjvsVr9mURkfWL4hu2b1_q5JzZx_92gVeGPx7wt4h9C3-1w6o41mT7D9GFCJPq9qv9hZAnxxDMc36YPliHhr1epP049AyyvDR1K-9DtgOx8DfVf0_H-iUDD6icCgtcfsVmlfm7FsZR_A81fv-Z_HZBg9Er6b6ADlj_Xr-WvDkDON671hwCw-nF0_Pwz4Ja_3lCkt-uP43FnSiYx1PirAf6M_zrBX7q_EMBZ3wqCIPTjGNxY64JHiQujSJTI1PzURwBfmh8IIMHH0-N53komoMxGgg3ZywyWZfED0A3HmtXSXac9eRAsTB2Nh76pgWjTBMtD0NIkFlwTt3AZtChg9MtJbNRWLouB4wiAMW0b8YiOO7rEgq1XfahWo4YDLu2GWiBE5oNZi6I-kbFsMjBqFup3OgawpriFj6ku66sEHbzXqsYGLw5gsjApTjU4uAUQgcrqAXALjq7jVX2ZjxhgSKkEMNXxgrmMUJxJQ9I4fq39b6cE78osWDImiayiRF8ItvuybUJsT_l_378nlliRim2Z_SzVp187UgP2pdiLZspFshW7UpltTueNaZ6v0rLY3bwrq0O6zsuT8p4fijJtwI9V-l4c0jJbZ-qzuPTZ3UufiH-Vhzw7qtH2vIqt1fAPd6q-bOiIMLXd0Bm-CrNpuTxvf4X69CXbGEN_c4sUMeQvm-ZxtmlCk3EGlDGua3rLNERNCy-s7QvlIoBdtsh22a75YyeW32VZvu3_aUADjsdj87UoXtdZc1ZsGvA7lWWxF97fItW3zYbTU448ymrSufPpHU_03R4pyYv49rNH69u3_wFiRv36/dz/d5/L0lDUmlTUSEhL3dHa0FKRnNBLzROV3FpQSEhL3Nr/"""

#'None, None' chyba
"""https://slovak.statistics.sk/wps/portal/ext/products/informationmessages/inf_sprava_detail/446bf649-5a39-4790-9dd4-f52fc66ba32f/!ut/p/z1/rZNLc5swFIX_SrrwUqMLEq8l9iQY1_YUHBxbm4542RQbiFFJ6K-viKfTdqY8FmUjGN17dHTuB2b4gFnBm-zERVYW_CK_j0z_6hmuOZ8rNsB8TcBdfd5tl4sn1Qk0_PJ3gbn1H8F9tr84_ooqQDXM5Lbted5uvd-Ds1efwCWKA9sgkGo63mOGWVSISpzxsQxrfkZ1jrIiRTwXM5Av5e0q3TRFgurqxpt2Bk2diFyulOphqlMLaZxYiBoWICuOKUo1NY10PeRETTv5KspifJxUfb_OgF82JY6FYy-psQYw144Grr0MfMsjBGwyFse9H3oeG6b1Dxhkw_IvXV4jNxjTYIMmn3W8q3N8lEaN3iJfJtlkyRsOim78F7z7PUct1RSiUkBpnOiI0khFlspNZGhpGKmgEBJpeAl4NZaVZFu9bRabk1Tm4txBV-JDzgW_lKeHP8hro_PDB3tdS_bt9ZXZktmyEMm7wIdf0M6gFrI8Qh87hYS3upXx91y0PRgPnnTPp2-QitGfzyTOV2Mg_zucSdpDIf3PP7u6BleTtFmWodw3N4-EsrAlP-ZbJNc3-9NPw5kCuA!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/"""
# endregion
