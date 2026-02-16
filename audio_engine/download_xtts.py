import os
from TTS.utils.manage import ModelManager
from TTS.api import TTS

# Bypass interactive terms of service for this download
os.environ["COQUI_TOS_AGREED"] = "1"
print("Starting XTTS v2 download...")
TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
