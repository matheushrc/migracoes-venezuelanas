import string
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator
from pydantic_ai.usage import RunUsage

type InferenceType = Literal["IMAGE", "TEXT"]


class TokenUsage(BaseModel):
    input_tokens: int = Field(default=0)
    output_tokens: int = Field(default=0)
    total_tokens: int = Field(default=0)
    requests: int = Field(default=0)
    model_name: str = Field(default="unknown")

    @classmethod
    def from_run_usage(
        cls, run_usage: RunUsage, model_name: str = "unknown"
    ) -> TokenUsage:
        input_tokens = run_usage.request_tokens or 0
        output_tokens = run_usage.response_tokens or 0
        return cls(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            requests=run_usage.requests or 0,
            model_name=model_name,
        )


class InferenceCreate(BaseModel):
    inference_type: InferenceType = Field(
        "TEXT", description="Tipo de inferência a ser utilizado"
    )
    user_prompt: str = Field(
        ..., description="O prompt a ser enviado para o agente Google"
    )
    invoke_params: dict[str, str] | None = Field(
        None,
        description="Parâmetros adicionais para a invocação do agente, serão formatados no prompt_template",
    )
    image_list: bytes | list[bytes] | None = Field(
        None, description="Lista de imagens a serem enviadas junto com o prompt"
    )
    image_media_type: str = Field("image/jpeg", description="Tipo de mídia da imagem")

    message_history: list[Any] | None = Field(
        None,
        description="Histórico de mensagens opcional a ser incluído na chamada do agente",
    )

    @model_validator(mode="after")
    def check_inference_type(self):
        if self.inference_type == "IMAGE" and not self.image_list:
            raise ValueError(
                "A lista de imagens (image_list) é obrigatória quando o tipo de inferência (inference_type) for 'IMAGE'"
            )
        return self

    @model_validator(mode="after")
    def check_invoke_params(self):
        # Detecta placeholders no prompt_template
        placeholders = [
            name for _, name, _, _ in string.Formatter().parse(self.user_prompt) if name
        ]
        if self.inference_type == "TEXT" and placeholders:
            missing = []
            if self.invoke_params is None:
                missing = placeholders
            else:
                missing = [
                    p
                    for p in placeholders
                    if p not in self.invoke_params or self.invoke_params[p] is None
                ]
            if missing:
                raise ValueError(
                    f"Os parâmetros de invocação (invoke_params) são obrigatórios para os placeholders não preenchidos: {missing}"
                )
        return self
