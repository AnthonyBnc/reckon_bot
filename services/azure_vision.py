from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from config.settings import get_config_status, get_required_env


def analyse_image(image_bytes: bytes) -> dict:
    if not image_bytes:
        return _empty_result()

    if not get_config_status().vision_ready:
        return {
            "caption": "",
            "keywords": [],
            "ocr_text": "",
            "error": "Azure AI Vision is not configured. Add values to .env to enable image analysis.",
        }

    client = ImageAnalysisClient(
        endpoint=get_required_env("AZURE_VISION_ENDPOINT"),
        credential=AzureKeyCredential(get_required_env("AZURE_VISION_KEY")),
    )

    result = client.analyze(
        image_data=image_bytes,
        visual_features=[
            VisualFeatures.CAPTION,
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS,
            VisualFeatures.READ,
        ],
    )

    caption = ""
    if result.caption:
        caption = result.caption.text

    tags = [tag.name for tag in result.tags.list] if result.tags else []
    objects = [item.tags[0].name for item in result.objects.list if item.tags] if result.objects else []

    ocr_lines = []
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                ocr_lines.append(line.text)

    keywords = sorted(set(tags + objects))
    return {
        "caption": caption,
        "keywords": keywords,
        "ocr_text": " ".join(ocr_lines),
        "error": "",
    }


def _empty_result() -> dict:
    return {
        "caption": "",
        "keywords": [],
        "ocr_text": "",
        "error": "",
    }
