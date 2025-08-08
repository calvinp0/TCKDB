"""Tests for qcfile utility functions."""

from tckdb.backend.app.utils.qcfile_utils import (
    compress_bytes,
    decompress_bytes,
    generate_checksum,
)


def test_compress_decompress_and_checksum():
    data = b"quantum chemistry data"
    checksum = generate_checksum(data)
    compressed = compress_bytes(data)
    assert compressed != data
    decompressed = decompress_bytes(compressed)
    assert decompressed == data
    assert checksum == generate_checksum(decompressed)
