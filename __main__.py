import assemblyai as aai
import os

from src.Transcription import Transcription
from dotenv import load_dotenv

load_dotenv(".env")

ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY")

input_folder = "input_videos"
extracted_audio_folder = "extracted_audio"

aai.settings.api_key = ASSEMBLY_AI_API_KEY
config = aai.TranscriptionConfig(language_code="de")
transcriber = aai.Transcriber(config=config)

transcription = Transcription(transcriber)
# transcription.convert_videos(input_folder);
transcription.transcribe_audio_files(extracted_audio_folder)
