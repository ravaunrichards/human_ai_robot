import pytest

from software.conversation import (
    ConversationError,
    ConversationManager,
    EchoProvider,
    LocalLLMProvider,
    Message,
    OnlineProvider,
)


def test_message_role_validation():
    with pytest.raises(ValueError):
        Message("robot", "hi")


def test_echo_provider_offline():
    p = EchoProvider()
    assert not p.requires_internet
    out = p.generate([Message("user", "hello")])
    assert "hello" in out


def test_local_provider_unavailable_without_runner():
    p = LocalLLMProvider(runner=None)
    assert not p.available()
    with pytest.raises(ConversationError):
        p.generate([Message("user", "hi")])


def test_local_provider_with_runner():
    p = LocalLLMProvider(runner=lambda msgs: "local-reply")
    assert p.available()
    assert p.generate([Message("user", "hi")]) == "local-reply"


def test_online_provider_requires_key_and_client():
    assert not OnlineProvider(client=None, api_key=None).available()
    assert not OnlineProvider(client=lambda m: "x", api_key=None).available()
    assert OnlineProvider(client=lambda m: "x", api_key="k").available()


def test_manager_falls_back_to_echo_when_online_fails():
    def failing_client(msgs):
        raise RuntimeError("network down")
    online = OnlineProvider(client=failing_client, api_key="k")
    mgr = ConversationManager([online])
    out = mgr.reply("are you there?")
    assert "[offline-echo]" in out
    assert mgr.last_fell_back is True
    assert mgr.last_provider == "echo"


def test_manager_uses_primary_when_available():
    local = LocalLLMProvider(runner=lambda msgs: "primary")
    mgr = ConversationManager([local])
    out = mgr.reply("hi")
    assert out == "primary"
    assert mgr.last_fell_back is False


def test_manager_history_trim():
    mgr = ConversationManager([EchoProvider()], history_limit=4)
    mgr.add_system("sys")
    for i in range(10):
        mgr.reply(f"m{i}")
    # system message preserved, rest trimmed
    assert any(m.role == "system" for m in mgr.history)
    non_system = [m for m in mgr.history if m.role != "system"]
    assert len(non_system) <= 4
