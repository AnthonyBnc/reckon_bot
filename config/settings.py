import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class AzureConfigStatus:
    vision_ready: bool
    speech_ready: bool
    vision_endpoint: str
    speech_region: str


def get_config_status() -> AzureConfigStatus:
    vision_endpoint = os.getenv("AZURE_VISION_ENDPOINT", "").strip()
    vision_key = os.getenv("AZURE_VISION_KEY", "").strip()
    speech_key = os.getenv("AZURE_SPEECH_KEY", "").strip()
    speech_region = os.getenv("AZURE_SPEECH_REGION", "").strip()

    return AzureConfigStatus(
        vision_ready=bool(vision_endpoint and vision_key),
        speech_ready=bool(speech_key and speech_region),
        vision_endpoint=vision_endpoint,
        speech_region=speech_region,
    )


def get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value
