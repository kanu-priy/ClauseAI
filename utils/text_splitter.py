from typing import List


def split_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks for processing long contracts.

    Args:
        text: The full contract text
        chunk_size: Max characters per chunk
        overlap: Character overlap between consecutive chunks

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at a sentence boundary
        if end < len(text):
            # Look for sentence end (. or \n) near the chunk boundary
            boundary = text.rfind('\n', start, end)
            if boundary == -1 or boundary < start + chunk_size // 2:
                boundary = text.rfind('. ', start, end)
            if boundary != -1 and boundary > start + chunk_size // 2:
                end = boundary + 1

        chunks.append(text[start:end].strip())
        start = end - overlap  # overlap for context continuity

    return [c for c in chunks if c]


def get_best_chunk(text: str, max_chars: int = 5000) -> str:
    """
    For single-pass analysis, return the most content-rich portion of the contract.
    Prioritizes the beginning (definitions, parties) but includes the end (signatures, special terms).
    """
    if len(text) <= max_chars:
        return text

    # Take first 70% from beginning, last 30% from end
    front = int(max_chars * 0.70)
    back = int(max_chars * 0.30)

    return text[:front] + "\n\n[... middle section omitted for brevity ...]\n\n" + text[-back:]


def estimate_tokens(text: str) -> int:
    """Rough estimate: ~4 characters per token."""
    return len(text) // 4
