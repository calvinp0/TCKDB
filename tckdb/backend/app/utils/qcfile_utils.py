"""Utility functions for handling quantum chemistry files."""

import gzip
import hashlib


def compress_bytes(data: bytes) -> bytes:
    """Compress bytes using gzip."""
    return gzip.compress(data)


def decompress_bytes(data: bytes) -> bytes:
    """Decompress gzip-compressed bytes."""
    return gzip.decompress(data)


def generate_checksum(data: bytes, algorithm: str = "sha256") -> str:
    """Generate a checksum for the given data.

    Args:
        data: The bytes to checksum.
        algorithm: Hash algorithm to use (default: sha256).

    Returns:
        The hex digest string of the checksum.
    """
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()
