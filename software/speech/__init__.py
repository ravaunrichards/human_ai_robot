"""Modular speech interfaces: STT, TTS, VAD and audio devices.

All classes are hardware/back-end neutral. Concrete engines (Vosk,
Whisper, Piper, espeak, PortAudio, etc.) are injected or subclassed. No
audio engine is bundled; offline-capable options are documented in
docs/system_architecture/ai_architecture.md.
"""

from .stt import SpeechToText, STTError, NullSTT
from .tts import TextToSpeech, TTSError, NullTTS
from .vad import VoiceActivityDetector, EnergyVAD
from .audio_device import AudioDevice, NullAudioDevice

__all__ = [
    "SpeechToText",
    "STTError",
    "NullSTT",
    "TextToSpeech",
    "TTSError",
    "NullTTS",
    "VoiceActivityDetector",
    "EnergyVAD",
    "AudioDevice",
    "NullAudioDevice",
]
