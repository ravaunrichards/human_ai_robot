import logging

from software.diagnostics import FaultCode, FaultLog, HealthMonitor
from software.diagnostics.logging_setup import StructuredFormatter


def test_fault_log_record_and_latest():
    fl = FaultLog()
    fl.record(FaultCode.WATCHDOG_TIMEOUT, "no heartbeat")
    assert fl.latest().code is FaultCode.WATCHDOG_TIMEOUT
    assert len(fl.events()) == 1


def test_fault_log_trims():
    fl = FaultLog(max_events=5)
    for i in range(10):
        fl.record(FaultCode.COMM_LOST, str(i))
    assert len(fl.events()) == 5


def test_health_monitor_all_pass():
    hm = HealthMonitor()
    hm.register("a", lambda: (True, "ok"))
    hm.register("b", lambda: True)
    report = hm.run()
    assert report.healthy
    assert report.failed() == []


def test_health_monitor_check_exception_is_failure():
    hm = HealthMonitor()
    def boom():
        raise RuntimeError("x")
    hm.register("bad", boom)
    report = hm.run()
    assert not report.healthy
    assert "bad" in report.failed()


def test_structured_formatter_outputs_json():
    rec = logging.LogRecord("n", logging.INFO, __file__, 1, "hello", None, None)
    out = StructuredFormatter().format(rec)
    assert '"msg": "hello"' in out
    assert '"level": "INFO"' in out
