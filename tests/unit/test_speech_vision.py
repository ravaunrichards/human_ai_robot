from software.speech import EnergyVAD, NullAudioDevice, NullSTT, NullTTS
from software.vision import NullCamera, PerceptionConfig, PerceptionLayer


def test_null_stt_unavailable():
    s = NullSTT()
    assert not s.available()
    assert s.transcribe(b"\x00\x00") == ""


def test_null_tts_returns_silence():
    t = NullTTS()
    assert not t.available()
    audio = t.synthesize("hello")
    assert isinstance(audio, bytes)
    assert set(audio) <= {0}


def test_energy_vad_detects_loud_vs_silence():
    vad = EnergyVAD(threshold_rms=100.0)
    silence = b"\x00\x00" * 100
    loud = (b"\xff\x7f") * 100  # ~max positive int16
    assert not vad.is_speech(silence)
    assert vad.is_speech(loud)


def test_null_audio_device():
    d = NullAudioDevice()
    assert not d.available()
    assert d.read(10) == b"\x00\x00" * 10
    d.write(b"abcd")
    assert d.written == 4


def test_perception_disabled_by_default():
    layer = PerceptionLayer()
    cam = NullCamera()
    frame = cam.grab()
    assert layer.process(frame) == []
    assert layer.describe_scene(frame) == "perception disabled"


def test_perception_enabled_no_backend():
    layer = PerceptionLayer(PerceptionConfig(enabled=True))
    frame = NullCamera().grab()
    assert layer.describe_scene(frame) == "no perception backend installed"
    assert not layer.backend_installed()


def test_perception_privacy_defaults():
    cfg = PerceptionConfig()
    assert cfg.enabled is False
    assert cfg.allow_face_detection is False
    assert cfg.persist_frames is False
