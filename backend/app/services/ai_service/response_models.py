from typing import Union

from pydantic import BaseModel, Field


class TestLiteLLMPoem(BaseModel):
    poem: str


class TopicsResponse(BaseModel):
    chain_of_thought: Union[str, None] = (
        Field(
            None,
            description="A detailed explanation or reasoning process related to the topics. Can be None.",
        ),
    )

    topics: list[Union[str, None]] = Field(
        None,
        examples=[
            [
                "Priemerné ceny pohonných látok v SR",
                "Porovnanie cien s predchádzajúcimi týždňami",
                "Vplyv cien pohonných látok na ekonomiku",
                "Regulácie vlády v oblasti pohonných látok",
                "Správanie spotrebiteľov pri nákupe pohonných látok",
            ]
        ],
    )


class ArticleResponse(BaseModel):
    headlines: list[Union[str, None]] = Field(
        None,
        examples=[
            [
                "Ceny palív stagnujú na Slovensku",
                "Dopyt po pohonných látkach v 41. týždni",
                "Analýza: Ceny benzínu a nafty v SR",
            ]
        ],
    )
    perex: Union[str, None] = (
        Field(
            None,
            examples=[
                "Ceny pohonných látok na Slovensku sa v 41. týždni 2024 stabilizovali."
                " Zistite, čo stojí za týmto trendom a aké sú aktuálne ceny."
            ],
        ),
    )
    article: Union[str, None] = (
        Field(
            None,
            examples=[
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
                "tankovaní, snažiac sa nájsť najlepšie ceny."
            ],
        ),
    )
