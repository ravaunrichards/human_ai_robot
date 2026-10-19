# Automated Test Report

Generated: 2026-10-20 06:09:50

```
sss..................................................................... [ 94%]
....                                                                     [100%]
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/integration/test_convo_motion_diag.py::test_ai_reply_does_not_move_hardware
PASSED tests/integration/test_convo_motion_diag.py::test_bounded_intention_flows_through_planner
PASSED tests/integration/test_convo_motion_diag.py::test_health_reflects_estop
PASSED tests/safety/test_planner_safety.py::test_motion_disabled_by_default
PASSED tests/safety/test_planner_safety.py::test_valid_request_not_dispatched_when_disabled
PASSED tests/safety/test_planner_safety.py::test_cannot_enable_without_ack
PASSED tests/safety/test_planner_safety.py::test_cannot_enable_with_unverified_limits
PASSED tests/safety/test_planner_safety.py::test_bad_ack_token_rejected
PASSED tests/safety/test_planner_safety.py::test_out_of_range_rejected
PASSED tests/safety/test_planner_safety.py::test_unknown_joint_rejected
PASSED tests/safety/test_planner_safety.py::test_over_velocity_rejected
PASSED tests/safety/test_planner_safety.py::test_full_enable_then_dispatch
PASSED tests/safety/test_planner_safety.py::test_estop_blocks_dispatch
PASSED tests/safety/test_safety_gate.py::test_default_gate_forbids_motion
PASSED tests/safety/test_safety_gate.py::test_gate_permits_only_when_everything_satisfied
PASSED tests/safety/test_safety_gate.py::test_simulation_only_always_blocks
PASSED tests/safety/test_safety_gate.py::test_estop_blocks_motion
PASSED tests/unit/test_config.py::test_defaults_simulation_only
PASSED tests/unit/test_config.py::test_env_override_bool
PASSED tests/unit/test_config.py::test_api_keys_from_env_only
PASSED tests/unit/test_config.py::test_invalid_motion_default_rejected
PASSED tests/unit/test_config.py::test_unknown_provider_rejected
PASSED tests/unit/test_config.py::test_load_from_file
PASSED tests/unit/test_conversation.py::test_message_role_validation
PASSED tests/unit/test_conversation.py::test_echo_provider_offline
PASSED tests/unit/test_conversation.py::test_local_provider_unavailable_without_runner
PASSED tests/unit/test_conversation.py::test_local_provider_with_runner
PASSED tests/unit/test_conversation.py::test_online_provider_requires_key_and_client
PASSED tests/unit/test_conversation.py::test_manager_falls_back_to_echo_when_online_fails
PASSED tests/unit/test_conversation.py::test_manager_uses_primary_when_available
PASSED tests/unit/test_conversation.py::test_manager_history_trim
PASSED tests/unit/test_diagnostics.py::test_fault_log_record_and_latest
PASSED tests/unit/test_diagnostics.py::test_fault_log_trims
PASSED tests/unit/test_diagnostics.py::test_health_monitor_all_pass
PASSED tests/unit/test_diagnostics.py::test_health_monitor_check_exception_is_failure
PASSED tests/unit/test_diagnostics.py::test_structured_formatter_outputs_json
PASSED tests/unit/test_joint_limits.py::test_joint_limit_contains_and_clamp
PASSED tests/unit/test_joint_limits.py::test_bad_limit_min_ge_max
PASSED tests/unit/test_joint_limits.py::test_bad_limit_velocity
PASSED tests/unit/test_joint_limits.py::test_load_json_limits
PASSED tests/unit/test_joint_limits.py::test_load_missing_field
PASSED tests/unit/test_joint_limits.py::test_load_empty_joints
PASSED tests/unit/test_joint_limits.py::test_load_file_not_found
PASSED tests/unit/test_motion_models.py::test_valid_joint_command
PASSED tests/unit/test_motion_models.py::test_non_finite_position_rejected[nan]
PASSED tests/unit/test_motion_models.py::test_non_finite_position_rejected[inf]
PASSED tests/unit/test_motion_models.py::test_non_finite_position_rejected[-inf]
PASSED tests/unit/test_motion_models.py::test_empty_joint_name_rejected
PASSED tests/unit/test_motion_models.py::test_non_numeric_position_rejected
PASSED tests/unit/test_motion_models.py::test_zero_or_negative_velocity_rejected
PASSED tests/unit/test_motion_models.py::test_empty_request_rejected
PASSED tests/unit/test_motion_models.py::test_duplicate_joint_rejected
PASSED tests/unit/test_motion_models.py::test_non_jointcommand_rejected
PASSED tests/unit/test_motion_models.py::test_bad_deadline_rejected
PASSED tests/unit/test_motion_models.py::test_as_dict_roundtrip_fields
PASSED tests/unit/test_protocol.py::test_encode_decode_roundtrip
PASSED tests/unit/test_protocol.py::test_incomplete_frame_returns_none
PASSED tests/unit/test_protocol.py::test_corrupt_crc_raises
PASSED tests/unit/test_protocol.py::test_bad_start_bytes_raise
PASSED tests/unit/test_protocol.py::test_payload_too_long_rejected
PASSED tests/unit/test_protocol.py::test_crc_is_deterministic
PASSED tests/unit/test_simulated_hardware.py::test_commands_rejected_when_disabled
PASSED tests/unit/test_simulated_hardware.py::test_enable_then_command
PASSED tests/unit/test_simulated_hardware.py::test_estop_blocks_and_disables
PASSED tests/unit/test_simulated_hardware.py::test_clear_estop_allows_reenable
PASSED tests/unit/test_simulated_hardware.py::test_watchdog_expiry_disables
PASSED tests/unit/test_speech_vision.py::test_null_stt_unavailable
PASSED tests/unit/test_speech_vision.py::test_null_tts_returns_silence
PASSED tests/unit/test_speech_vision.py::test_energy_vad_detects_loud_vs_silence
PASSED tests/unit/test_speech_vision.py::test_null_audio_device
PASSED tests/unit/test_speech_vision.py::test_perception_disabled_by_default
PASSED tests/unit/test_speech_vision.py::test_perception_enabled_no_backend
PASSED tests/unit/test_speech_vision.py::test_perception_privacy_defaults
SKIPPED [1] tests/hardware/test_real_hardware.py:21: requires commissioned physical hardware (ROBOT_HARDWARE_PRESENT=1)
SKIPPED [1] tests/hardware/test_real_hardware.py:25: requires commissioned physical hardware (ROBOT_HARDWARE_PRESENT=1)
SKIPPED [1] tests/hardware/test_real_hardware.py:29: requires commissioned physical hardware (ROBOT_HARDWARE_PRESENT=1)
73 passed, 3 skipped in 0.38s
```
