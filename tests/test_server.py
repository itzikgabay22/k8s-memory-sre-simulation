from __future__ import annotations

import pytest

from app.server import allocate_memory, parse_memory_mb


def test_parse_memory_mb_defaults_to_zero() -> None:
    assert parse_memory_mb(None) == 0
    assert parse_memory_mb("") == 0


def test_parse_memory_mb_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        parse_memory_mb("-1")


def test_allocate_memory_uses_mebibytes() -> None:
    memory = allocate_memory(1)

    assert memory is not None
    assert len(memory) == 1024 * 1024
