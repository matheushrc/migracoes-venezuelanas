from typing import Any, Dict, Optional, Type, Union

from google import genai
from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent, Tool
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider

from src.models import InferenceCreate


class GoogleAgent:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def create_agent(
        self,
        output_type: Optional[Union[Type[BaseModel], type, str]] = str,
        model_name: str = "gemini-flash-lite-latest",
        retries: int = 3,
        model_settings: Optional[Dict[str, Any]] = {
            "temperature": 1,
            "max_tokens": 65535,
            "top_p": 0.95,
        },
        system_prompt: Optional[str] = None,
        tools: Optional[list[Tool]] = None,
    ) -> Agent:
        agent_kwargs: dict[str, Any] = {
            "output_type": output_type,
            "retries": retries,
        }

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
        )

    def get_inference(self, inference_data: InferenceCreate, agent: Agent) -> Any:
        if inference_data.invoke_params:
            inference_data.user_prompt = inference_data.user_prompt.format(
                **inference_data.invoke_params
            )

        # Prepare message content with prompt
        message_content: list[Union[str, BinaryContent]] = [inference_data.user_prompt]

        # Add image if provided
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

        # Run the agent with the content. If a message history is provided,
        # pass it as `messages` so the agent can use it as context for follow-up runs.
        run_kwargs = {}
        if inference_data.message_history:
            # pydantic-ai expects the parameter name `message_history` for prior messages
            run_kwargs["message_history"] = inference_data.message_history

        run_input = (
            message_content
            if inference_data.inference_type == "IMAGE"
            else inference_data.user_prompt
        )

        response = agent.run_sync(
            user_prompt=run_input,
            **run_kwargs,
        )
        return getattr(response, "output", response)

    def run_stream(self, inference_data: InferenceCreate, agent: Agent):
        if inference_data.invoke_params:
            inference_data.user_prompt = inference_data.user_prompt.format(
                **inference_data.invoke_params
            )

        # Prepare message content with prompt
        message_content: list[Union[str, BinaryContent]] = [inference_data.user_prompt]

        # Add image if provided
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

        # Run the agent with the content
        run_kwargs = {}
        if inference_data.message_history:
            run_kwargs["message_history"] = inference_data.message_history

        run_input = (
            message_content
            if inference_data.inference_type == "IMAGE"
            else inference_data.user_prompt
        )

        return agent.run_stream(user_prompt=run_input, **run_kwargs)
