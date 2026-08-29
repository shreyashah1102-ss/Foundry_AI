import asyncio
import os
import sys

from agent_framework import Message
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv


load_dotenv(override=False)
sys.stdout.reconfigure(encoding="utf-8")

PROMPT = "Tell me a joke"


async def main():
    project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT") or os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    model = (
        os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
        or os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME")
        or os.getenv("FOUNDRY_MODEL")
    )

    if not project_endpoint or not model:
        raise RuntimeError(
            "Set FOUNDRY_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME in your environment or .env file."
        )

    async with AzureCliCredential() as credential:
        client = FoundryChatClient(
            project_endpoint=project_endpoint,
            model=model,
            credential=credential,
        )
        result = await client.get_response(
            [
                Message(
                    "system",
                    ["You are good at telling jokes. You also translate your answers into Hindi."],
                ),
                Message("user", [PROMPT]),
            ]
        )
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
