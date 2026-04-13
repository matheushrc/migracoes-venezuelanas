from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field

type Movimentos = Literal[
    "Admissão",
    "Desligamento",
]

type MotivosFatuaisEconomicos = Literal[
    "Apoio Institucional e Humanitário",
    "Busca por Oportunidades Financeiras",
    "Escassez e Condições Básicas de Sobrevivência",
]

type MotivosPoliticosAfetivos = Literal[
    "Reunificação e Laços Familiares",
    "Redes de Apoio Comunitário e Religioso",
    "Clima Político e Insegurança",
]


class MotivacoesFatuaisEconomicos(BaseModel):
    """Motivações de migração baseadas em condições objetivas e materiais (dimensão da Realidade)."""

    motivo: MotivosFatuaisEconomicos
    trechos: list[Annotated[str, Field(min_length=10)]] = Field(
        ...,
        min_length=1,
        description="Trechos verbatim do depoimento que evidenciam este motivo. Cada item é uma frase ou parágrafo copiado diretamente da entrevista.",
        examples=[["[...] trecho_onde_se_encontra_o_motivo [...]"]],
    )


class MotivacoesPoliticosAfetivos(BaseModel):
    """Motivações de migração baseadas em percepções subjetivas, emoções, crenças ou perseguição política (dimensão da Percepção/Afeto)."""

    motivo: MotivosPoliticosAfetivos
    trechos: list[Annotated[str, Field(min_length=10)]] = Field(
        ...,
        min_length=1,
        description="Trechos verbatim do depoimento que evidenciam este motivo. Cada item é uma frase ou parágrafo copiado diretamente da entrevista.",
        examples=[["[...] trecho_onde_se_encontra_o_motivo [...]"]],
    )


class Localidade(BaseModel):
    """Representação geográfica de uma cidade, com estado/província e país."""

    cidade: str = Field(
        ...,
        description="Nome da cidade.",
        examples=["Caracas", "Boa Vista", "Manaus"],
    )
    estado_provincia: str | None = Field(
        None,
        description="Sigla do estado ou província.",
        examples=["RR", "AM", "Miranda"],
    )
    pais: str = Field(
        ...,
        description="Código do país no formato ISO 3166-1 alpha-3.",
        examples=["BRA", "VEN", "COL"],
        pattern=r"^[A-Z]{3}$",
    )


class Movimentacao(BaseModel):
    """Registro de um cargo ou vínculo trabalhista da pessoa entrevistada."""

    descricao_atividade: str = Field(
        ...,
        description="Descrição da atividade ou cargo ocupado pela pessoa entrevistada.",
        examples=["Pedreiro", "Vendedor ambulante", "Auxiliar de cozinha"],
    )
    localidade: Localidade = Field(
        ...,
        description="Local onde a atividade ou cargo foi exercido.",
    )
    setor_atividade: str | None = Field(
        None,
        description="Código da classe CNAE do setor de atividade. Preenchido por etapa posterior do pipeline — retorne sempre null.",
    )
    tipo_movimento: Movimentos = Field(
        ...,
        description="Tipo de evento trabalhista: entrada (Admissão) ou saída (Desligamento) do vínculo.",
    )
    motivo_movimento: str = Field(
        ...,
        description="Motivo que gerou o evento trabalhista.",
        examples=[
            "Demissão voluntária por busca de melhor salário",
            "Término de contrato temporário",
        ],
    )
    ano: int | None = Field(
        None,
        description="Ano em que o evento trabalhista ocorreu.",
        examples=[2018, 2021],
        ge=1900,
        le=2100,
    )


class Deslocamento(BaseModel):
    """Parada em uma localidade durante a rota de migração da pessoa entrevistada."""

    localidade: Localidade = Field(
        ...,
        description="Localidade onde a pessoa esteve durante o deslocamento.",
    )
    data: date | None = Field(
        None,
        description="Data aproximada de chegada nesta localidade.",
        examples=["2019-03-01", "2020-11-15"],
    )
    motivo: str = Field(
        ...,
        description="Razão pela qual a pessoa se deslocou para esta localidade.",
        examples=[
            "Busca de emprego",
            "Passagem em rota para o Brasil",
            "Reunificação familiar",
        ],
    )


class Entrevista(BaseModel):
    """Dados estruturados extraídos de uma entrevista com migrante venezuelano."""

    motivos_fatuais_economicos: list[MotivacoesFatuaisEconomicos] = Field(
        ...,
        description="Lista de motivações fatuais/econômicas identificadas na entrevista. Um item por motivo distinto.",
    )
    motivos_politicos_afetivos: list[MotivacoesPoliticosAfetivos] = Field(
        ...,
        description="Lista de motivações político-afetivas identificadas na entrevista. Um item por motivo distinto.",
    )
    movimentacoes: list[Movimentacao] = Field(
        ...,
        description="Histórico de vínculos trabalhistas da pessoa entrevistada, em ordem cronológica quando possível.",
    )
    deslocamento: list[Deslocamento] = Field(
        ...,
        description="Sequência cronológica de localidades percorridas pela pessoa desde a origem até o destino final.",
    )
