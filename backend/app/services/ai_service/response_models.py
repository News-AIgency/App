from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class TestLiteLLMPoem(BaseModel):
    poem: str


class BaseResponse(BaseModel):
    chain_of_thought: Optional[str] = None


class TopicsResponse(BaseResponse):
    topics: list[str] = Field(
        None,
        description="Examples of topics:"
        "Priemerné ceny pohonných látok v SR, "
        "Porovnanie cien s predchádzajúcimi týždňami, "
        "Vplyv cien pohonných látok na ekonomiku, "
        "Regulácie vlády v oblasti pohonných látok, "
        "Správanie spotrebiteľov pri nákupe pohonných látok",
    )


class ArticleResponse(BaseResponse):
    headlines: list[str] = Field(
        None,
        description="Examples of headlines:"
        "Ceny palív stagnujú na Slovensku, "
        "Dopyt po pohonných látkach v 41. týždni, "
        "Analýza: Ceny benzínu a nafty v SR, ",
    )
    engaging_text: str = Field(
        None,
        description="Examples of engaging text:"
        "Priemerné ceny pohonných látok v SR v 41. týždni 2024 vzrástli. Benzín a nafta zdraželi v priemere o 2 centy na liter. "
        "Cena LPG stúpla, LNG klesla, CNG mierne zlacnel. Detaily zverejnil Štatistický úrad SR.",
    )
    perex: str = Field(
        None,
        description="Example of perex:"
        "Ceny pohonných látok na Slovensku sa v 41. týždni 2024 stabilizovali."
        " Zistite, čo stojí za týmto trendom a aké sú aktuálne ceny.",
    )
    article: str = Field(
        None,
        description="Examples of article:"
        "V 41. týždni 2024 sa na Slovensku ceny pohonných látok stabilizovali, pričom benzín a nafta "
        "udržali svoje hodnoty v porovnaní s predchádzajúcim týždňom. Podľa údajov zo spoločnosti "
        "májový prieskum ukázal, že priemerná cena benzínu sa pohybuje okolo 1,50 € za liter, "
        "zatiaľ čo cena nafty je približne 1,40 € za liter. Tieto ceny sú výsledkom globálneho trhu s "
        "ropou a miestnych dodávateľských podmienok. Na stretnutí s novinármi minulé pondelok, "
        'hovorca Ministerstva hospodárstva SR uviedol: "Ceny palív sú obyčajne ovplyvnené medzinárodným'
        ' trhom. V súčasnosti sme svedkami stabilného vývoja, čo je priaznivá správa pre vodičov." '
        "Vzhľadom na dopyt po pohonných látkach počas jeseň, očakáva sa, že ceny môžu byť pod tlakom. "
        "Špecialisti na trh predpovedajú potenciálne zvýšenie cien, ak dôjde k jeho narušeniu napríklad "
        "pre geopolitické faktory alebo zmeny v produkcii ropy. Taktiež, v niektorých regiónoch, "
        "ako sú Bratislava a Košice, sú ceny mierne vyššie, z dôvodu miestnej konkurencie a dopytu. "
        "Tento trend sa pozoruje už niekoľko týždňov, pričom motoristi sú naďalej obozretní pri "
        "tankovaní, snažiac sa nájsť najlepšie ceny.",
    )
    tags: list[str] = Field(
        None,
        description="Examples of tags: #cenyPohonnýchLátok"
        "#benzín"
        "#nafta"
        "#Slovensko",
    )
    gen_graph: bool = Field(
        None,
        description="Boolean value representing if a graph should be generated or not",
    )
    graph_type: Literal["pie", "line", "bar", "histogram", "scatter"] = Field(
        None,
        description="The type of the graph to generate from data in: pie, line, bar, histogram, scatter",
    )
    graph_data: dict[str, Any] = Field(
        None,
        description=(
            "Graph data in dict format. "
            "Structure depends on `graph_type`: \n"
            "- For 'pie', 'line', 'bar', 'histogram': include `labels` (None for histogram) and `values`\n"
            "- For 'scatter': include `x_vals` and `y_vals`\n"
            "Examples:\n"
            "- Pie: {'labels': [...], 'values': [...]} \n"
            "- Histogram: {'labels': None, 'values': [...]} \n"
            "- Scatter: {'x_vals': [...], 'y_vals': [...]} "
        ),
    )


class HeadlineResponse(BaseResponse):
    headlines: list[str] = Field(
        None,
        description="Examples of headlines:"
        "Ceny palív stagnujú na Slovensku, "
        "Dopyt po pohonných látkach v 41. týždni, "
        "Analýza: Ceny benzínu a nafty v SR, ",
    )


class EngagingTextResponse(BaseResponse):
    engaging_text: str = Field(
        None,
        description="Examples of engaging text:"
        "Priemerné ceny pohonných látok v SR v 41. týždni 2024 vzrástli. Benzín a nafta zdraželi v priemere o 2 centy na liter. "
        "Cena LPG stúpla, LNG klesla, CNG mierne zlacnel. Detaily zverejnil Štatistický úrad SR.",
    )


class PerexResponse(BaseResponse):
    perex: str = Field(
        None,
        description="Example of perex:"
        "Ceny pohonných látok na Slovensku sa v 41. týždni 2024 stabilizovali."
        " Zistite, čo stojí za týmto trendom a aké sú aktuálne ceny.",
    )


class ArticleBodyResponse(BaseResponse):
    article: str = Field(
        None,
        description="Examples of article:"
        "V 41. týždni 2024 sa na Slovensku ceny pohonných látok stabilizovali, pričom benzín a nafta "
        "udržali svoje hodnoty v porovnaní s predchádzajúcim týždňom. Podľa údajov zo spoločnosti "
        "májový prieskum ukázal, že priemerná cena benzínu sa pohybuje okolo 1,50 € za liter, "
        "zatiaľ čo cena nafty je približne 1,40 € za liter. Tieto ceny sú výsledkom globálneho trhu s "
        "ropou a miestnych dodávateľských podmienok. Na stretnutí s novinármi minulé pondelok, "
        'hovorca Ministerstva hospodárstva SR uviedol: "Ceny palív sú obyčajne ovplyvnené medzinárodným'
        ' trhom. V súčasnosti sme svedkami stabilného vývoja, čo je priaznivá správa pre vodičov." '
        "Vzhľadom na dopyt po pohonných látkach počas jeseň, očakáva sa, že ceny môžu byť pod tlakom. "
        "Špecialisti na trh predpovedajú potenciálne zvýšenie cien, ak dôjde k jeho narušeniu napríklad "
        "pre geopolitické faktory alebo zmeny v produkcii ropy. Taktiež, v niektorých regiónoch, "
        "ako sú Bratislava a Košice, sú ceny mierne vyššie, z dôvodu miestnej konkurencie a dopytu. "
        "Tento trend sa pozoruje už niekoľko týždňov, pričom motoristi sú naďalej obozretní pri "
        "tankovaní, snažiac sa nájsť najlepšie ceny.",
    )


class TagsResponse(BaseResponse):
    tags: list[str] = Field(
        None,
        description="Examples of tags: #cenyPohonnýchLátok"
        "#benzín"
        "#nafta"
        "#Slovensko",
    )


class GraphResponse(BaseResponse):
    gen_graph: bool = Field(
        None,
        description="Boolean value representing if a graph should be generated or not",
    )
    graph_type: Literal["pie", "line", "bar", "histogram", "scatter"] = Field(
        None,
        description="The type of the graph to generate from data in: pie, line, bar, histogram, scatter",
    )
    graph_data: dict[str, Any] = Field(
        None,
        description=(
            "Graph data in dict format. "
            "Structure depends on `graph_type`: \n"
            "- For 'pie', 'line', 'bar', 'histogram': include `labels` (None for histogram) and `values`\n"
            "- For 'scatter': include `x_vals` and `y_vals`\n"
            "Examples:\n"
            "- Pie: {'labels': [...], 'values': [...]} \n"
            "- Histogram: {'labels': None, 'values': [...]} \n"
            "- Scatter: {'x_vals': [...], 'y_vals': [...]} "
        ),
    )
