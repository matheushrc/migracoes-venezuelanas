import json
import os
import re
from glob import glob
from typing import List, Union, get_args

import logfire
from dotenv import load_dotenv
from loguru import logger
from pydantic_ai.models.google import LatestGoogleModelNames

from src.agents import GoogleAgent
from src.models import Entrevista, InferenceCreate
from src.prompts import ENTREVISTA_PROMPT
from src.tools import get_coordinates

logfire.configure()
logfire.instrument_pydantic_ai()
load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

google_agent = GoogleAgent(api_key=GOOGLE_API_KEY)

# Extract all available model names from the Literal type
AVAILABLE_GOOGLE_MODELS = get_args(LatestGoogleModelNames)

entrevista_agent = google_agent.create_agent(
    system_prompt=ENTREVISTA_PROMPT,
    output_type=Entrevista,
    model_name=AVAILABLE_GOOGLE_MODELS[10],  # gemini-3-pro-preview
    model_settings={
        "temperature": 0,
        "max_tokens": 65535,
    },
)


USER_PROMPT = """
<entrevista>
{entrevista_content}
</entrevista>
"""


async def process_interviews():

    entrevistas = os.listdir("data/entrevistas/clean/")
    # entrevistas = ["entrevista_8.clean.md"]
    logger.info(f"Total entrevistas to process: {entrevistas}")

    os.makedirs("outputs", exist_ok=True)

    for i, entevista in enumerate(entrevistas):
        logger.info(f"Processing entrevista {i + 1}/{len(entrevistas)}: {entevista}")
        with open(f"data/entrevistas/clean/{entevista}", "r", encoding="utf-8") as f:
            entrevista_content = f.read()

            response = await google_agent.get_inference(
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


def insert_coordinates(entrevistas: Union[List[str], str]):

    for i, entrevista in enumerate(entrevistas):
        logger.info(
            f"Adicionando coordenadas geográficas na entrevista {i + 1}/{len(entrevistas)}: {entrevista}"
        )
        with open(entrevista, "r", encoding="utf-8") as f:
            data = json.load(f)

            deslocamentos = data.get("deslocamento", [])

            novos_deslocamentos = [
                {
                    **deslocamento,
                    "geographic_coordinates": get_coordinates(
                        f"{deslocamento['localidade']['cidade']}-{deslocamento['localidade']['estado_provincia']}-{deslocamento['localidade']['pais']}"
                    ),
                }
                for deslocamento in deslocamentos
            ]

            data.update({"deslocamento": novos_deslocamentos})

        with open(entrevista, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def covert_to_csv(entrevistas: Union[List[str], str]):

    all_data = []

    for entrevista in entrevistas:
        with open(entrevista, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Convertendo entrevista para CSV: {entrevista}")
            id = os.path.basename(entrevista).replace(".json", "")
            deslocamentos = data.get("deslocamento", [])
            for deslocamento in deslocamentos:
                geographic_coordinates = deslocamento.get("geographic_coordinates", {})
                all_data.append({
                    "id": int(re.sub("[^0-9]", "", id)),
                    "address": geographic_coordinates.get("address", ""),
                    "latitude": geographic_coordinates.get("latitude", ""),
                    "longitude": geographic_coordinates.get("longitude", ""),
                })

    import pandas as pd

    df = pd.DataFrame(all_data)
    df.to_csv("outputs/entrevistas_coordinates.csv", index=False)


if __name__ == "__main__":
    import asyncio

    entrevistas = glob("./outputs/*.json")

    asyncio.run(process_interviews())
    insert_coordinates(entrevistas=entrevistas)
    covert_to_csv(entrevistas=entrevistas)
