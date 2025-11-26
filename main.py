import json
import os
from enum import Enum

from dotenv import load_dotenv
from loguru import logger

from src.agents import GoogleAgent
from src.models import Entrevista, InferenceCreate
from src.prompts import ENTREVISTA_PROMPT

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

google_agent = GoogleAgent(api_key=api_key)


class GeminiModels(str, Enum):
    # gemini-3-pro-preview
    GEMINI_3_PRO_PREVIEW = "gemini-3-pro-preview"
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"


entrevista_agent = google_agent.create_agent(
    system_prompt=ENTREVISTA_PROMPT,
    output_type=Entrevista,
    model_name=GeminiModels.GEMINI_2_5_FLASH_LITE,
    model_settings={
        "temperature": 0,
    },
)


USER_PROMPT = """
<entrevista>
{entrevista_content}
</entrevista>
"""


def main():

    entrevistas = os.listdir("data/entrevistas/clean/")
    # entrevistas = ["entrevista_8.clean.md"]
    logger.info(f"Total entrevistas to process: {entrevistas}")

    os.makedirs("outputs", exist_ok=True)

    for i, entevista in enumerate(entrevistas):
        logger.info(f"Processing entrevista {i + 1}/{len(entrevistas)}: {entevista}")
        with open(f"data/entrevistas/clean/{entevista}", "r", encoding="utf-8") as f:
            entrevista_content = f.read()

            response = google_agent.get_inference(
                inference_data=InferenceCreate(
                    user_prompt=USER_PROMPT,
                    invoke_params={"entrevista_content": entrevista_content},
                ),  # type: ignore
                agent=entrevista_agent,
            )

            with open(
                f"outputs/{os.path.basename(entevista).replace('md', 'json')}",
                "w",
                encoding="utf-8",
            ) as f:
                if hasattr(response, "model_dump") and callable(
                    getattr(response, "model_dump")
                ):
                    # response is a Pydantic model, use mode="json" to serialize date objects
                    response_dict = response.model_dump(mode="json")
                else:
                    response_dict = {"text": str(response)}
                json.dump(response_dict, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
