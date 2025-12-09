from datetime import date
from typing import List, Literal, Optional, TypeAlias

from pydantic import BaseModel, Field


class Motivacao(BaseModel):
    motivos_migracao: List[str] = Field(
        ...,
        description="Lista de motivos que levaram a pessoa entrevistada a migrar. Lista de palavras ou frases curtas.",
        examples=[
            "Busca por melhores oportunidades de emprego",
            "Reunificação familiar",
            "Fuga de violência ou perseguição",
        ],
    )


Movimentos: TypeAlias = Literal[
    "Admissão",
    "Desligamento",
]


class Localidade(BaseModel):
    cidade: str = Field(
        ..., description="Nome da cidade.", examples=["Caracas", "Boa Vista"]
    )
    estado_provincia: Optional[str] = Field(
        None, description="Sigla do estado ou província.", examples=["RR", "AM"]
    )
    pais: str = Field(
        ...,
        description="Sigla do país no formato ISO 3166-1 alpha-3. Ex: BRA, VEN.",
        examples=["BRA", "VEN"],
    )


# model para representar cargos ocupados e locais de trabalho
class Movimentacao(BaseModel):
    descricao_atividade: str = Field(
        ...,
        description="Descrição da atividade ou cargo ocupado pela pessoa entrevistada.",
    )
    localidade: Localidade = Field(
        ...,
        description="Local onde a pessoa entrevistada trabalhou.",
    )
    setor_atividade: Optional[str] = Field(
        None, description="Setor de atividade econômica do local de trabalho."
    )
    tipo_movimento: Movimentos = Field(
        ...,
        description="Tipo de movimento trabalhista relacionado ao cargo e local de trabalho.",
    )
    motivo_movimento: str = Field(
        ..., description="Motivo associado ao movimento trabalhista."
    )
    ano: Optional[int] = Field(
        ...,
        description="Ano em que o movimento trabalhista ocorreu. Se desconhecido, deixar None",
    )


class Deslocamento(BaseModel):
    localidade: Localidade = Field(
        ...,
        description="Localidade do deslocamento.",
    )
    data: Optional[date] = Field(
        ...,
        description="Data do deslocamento no formato AAAA-MM-DD. Se desconhecido, deixar None.",
    )
    motivo: str = Field(..., description="Motivo do deslocamento para esta localidade.")


class Entrevista(BaseModel):
    motivos_fatuais_economicos: List[str] = Field(
        ...,
        description="Lista de motivos baseados em condições objetivas ou materiais (Realidade), como falta de emprego, escassez de produtos básicos, ou busca por melhorias financeiras. Lista de palavras ou frases curtas.",
        examples=[
            "Falta de medicamentos essenciais",
            "Busca por melhores oportunidades de emprego",
            "Pobreza e fome",
        ],
    )
    motivos_politicos_afetivos: List[str] = Field(
        ...,
        description="Lista de motivos baseados em elementos subjetivos, emocionais, crenças ou perseguição política (Percepção/Afeto). Incluir fuga de violência, medo de repressão ou alinhamento político.",
        examples=[
            "Fuga de perseguição política",
            "Necessidade de coesão social fora do país",
            "Medo da violência estatal",
        ],
    )
    movimentacoes: List[Movimentacao] = Field(
        ...,
        description="Lista de movimentações trabalhistas da pessoa entrevistada.",
    )
    deslocamento: List[Deslocamento] = Field(
        ...,
        description="Lista de locais que a pessoa entrevistada passou durante seu deslocamento. Um deslocamento só acontece se ele sair de uma cidade a outra.",
    )
