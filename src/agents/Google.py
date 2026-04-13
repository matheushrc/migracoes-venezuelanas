from typing import Any

from google import genai
from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent, Tool
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider

from src.models import InferenceCreate, TokenUsage


class GoogleAgent:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def create_agent(
        self,
        deps_type: type[BaseModel] | None = None,
        output_type: type[BaseModel] | type | str | None = str,
        model_name: str = "gemini-flash-lite-latest",
        retries: int = 3,
        model_settings: dict[str, Any] | None = {
            "temperature": 1,
            "max_tokens": 65535,
            "top_p": 0.95,
        },
        system_prompt: str | None = None,
        tools: list[Tool] | None = None,
        **kwargs: Any,
    ) -> Agent:
        agent_kwargs: dict[str, Any] = {
            "output_type": output_type,
            "retries": retries,
        }
        if deps_type is not None:
            agent_kwargs["deps_type"] = deps_type
        if system_prompt is not None:
            agent_kwargs["system_prompt"] = system_prompt
        if model_settings:
            agent_kwargs["model_settings"] = GoogleModelSettings(**model_settings)
        if tools:
            agent_kwargs["tools"] = tools

        return Agent(
            model=GoogleModel(
                model_name=model_name,
                provider=GoogleProvider(
                    client=self.client,
                ),
            ),
            **agent_kwargs,
            **kwargs,
        )

    async def get_inference(
        self,
        inference_data: InferenceCreate,
        agent: Agent,
        model_name: str = "unknown",
    ) -> tuple[Any, TokenUsage]:
        if inference_data.invoke_params:
            inference_data.user_prompt = inference_data.user_prompt.format(
                **inference_data.invoke_params
            )

        message_content: list[str | BinaryContent] = [inference_data.user_prompt]

        if inference_data.image_list:
            if isinstance(inference_data.image_list, bytes):
                inference_data.image_list = [inference_data.image_list]
            for image in inference_data.image_list:
                if isinstance(image, bytes):
                    message_content.append(
                        BinaryContent(
                            data=image,
                            media_type=inference_data.image_media_type,
                        )
                    )

        run_kwargs = {}
        if inference_data.message_history:
            run_kwargs["message_history"] = inference_data.message_history

        run_input = (
            message_content
            if inference_data.inference_type == "IMAGE"
            else inference_data.user_prompt
        )

        response = await agent.run(
            user_prompt=run_input,
            **run_kwargs,
        )
        token_usage = TokenUsage.from_run_usage(response.usage(), model_name=model_name)
        return getattr(response, "output", response), token_usage

    def run_stream(self, inference_data: InferenceCreate, agent: Agent):
        if inference_data.invoke_params:
            inference_data.user_prompt = inference_data.user_prompt.format(
                **inference_data.invoke_params
            )

        message_content: list[str | BinaryContent] = [inference_data.user_prompt]

        if inference_data.image_list:
            if isinstance(inference_data.image_list, bytes):
                inference_data.image_list = [inference_data.image_list]
            for image in inference_data.image_list:
                if isinstance(image, bytes):
                    message_content.append(
                        BinaryContent(
                            data=image,
                            media_type=inference_data.image_media_type,
                        )
                    )

        run_kwargs = {}
        if inference_data.message_history:
            run_kwargs["message_history"] = inference_data.message_history

        run_input = (
            message_content
            if inference_data.inference_type == "IMAGE"
            else inference_data.user_prompt
        )

        return agent.run_stream(user_prompt=run_input, **run_kwargs)
