import os
import tempfile

import azure.cognitiveservices.speech as speechsdk

from config.settings import get_config_status, get_required_env


def transcribe_audio(audio_bytes: bytes) -> str:
    if not audio_bytes:
        return ""

    if not get_config_status().speech_ready:
        return ""

    speech_config = speechsdk.SpeechConfig(
        subscription=get_required_env("AZURE_SPEECH_KEY"),
        region=get_required_env("AZURE_SPEECH_REGION"),
    )
    speech_config.speech_recognition_language = "en-US"

    temp_path = _write_temp_audio(audio_bytes)
    try:
        audio_config = speechsdk.AudioConfig(filename=temp_path)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
        )
        result = recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        if result.reason == speechsdk.ResultReason.NoMatch:
            return ""
        return f"Speech recognition failed: {result.reason}"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def _write_temp_audio(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        return temp_audio.name
