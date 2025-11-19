import textwrap
from typing import Annotated, Literal, TypeAlias

from fastapi import (
    APIRouter,
    Form,
    status,
)
from pydantic import BaseModel, Field

router = APIRouter(prefix="/inference", tags=["inference"])
Status: TypeAlias = Literal["QUEUED", "PROCESSING", "COMPLETED", "FAILED"]


class OCRResponse(BaseModel):
    document_id: str = Field(..., description="ID do processamento do documento")
    ocr_id: str = Field(..., description="ID do job OCR")
    status: Status = Field(..., description="Status de ambos os trabalhos")
    message: str = Field(..., description="Mensagem de status")


InferenceType: TypeAlias = Literal["IMAGE", "TEXT"]


@router.post(
    "",
    response_model=OCRResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enfileira um documento de contrato para processamento de OCR.",
    description=textwrap.dedent("""
    **Enviar um trabalho de OCR para um documento de Contrato**

    Enfileira um documento de contrato para processamento de OCR. Este endpoint é simplificado pois contratos
    são associados apenas a um `contract_id`.

    **Parâmetros:**
    - **contract_id** (string, form): O ID do contrato
    - **contract_ocr_type** (ContratoOcrType, form): O tipo de processamento de OCR (AUTOFILL ou FULL)
    - **s3_key** (string, form): A chave S3 do documento carregado

    **Retorna:**
    - **document_id** (string): Um ID único para o trabalho de processamento do documento
    - **ocr_id** (string): Um ID único para a tarefa de OCR
    - **status** (string): O status inicial do trabalho (geralmente "QUEUED")
    - **message** (string): Uma mensagem de confirmação

    **Casos de Uso:**
    - Extrair informações chave de contratos automaticamente (AUTOFILL)
    - Realizar uma extração completa de texto em contratos (FULL)

    **Respostas de Erro:**
    - **400**: Parâmetros inválidos
    - **404**: O contrato especificado não existe
    - **500**: Fila SQS não configurada ou erro interno do servidor
    """),
    responses={
        status.HTTP_201_CREATED: {
            "model": OCRResponse,
            "description": "Trabalho de OCR de Contrato criado com sucesso",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Requisição inválida - parâmetros incorretos",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Contrato não encontrado",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": OCRResponse,
            "description": "Erro interno do servidor",
        },
    },
)
def create_inference(
    user_prompt: Annotated[
        str, Form(description="Prompt do usuário para a inferência")
    ],
):
    import os

    from agents import GoogleAgent
    from models import InferenceCreate

    api_key = os.environ.get("GOOGLE_API_KEY", "")

    google_agent = GoogleAgent(api_key=api_key)

    agent = google_agent.create_agent(system_prompt="You are a helpful assistant.")

    response = google_agent.get_inference(
        inference_data=InferenceCreate(
            user_prompt=user_prompt,
        ),  # type: ignore
        agent=agent,
    )

    return response
