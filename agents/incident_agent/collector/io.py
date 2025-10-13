from typing import Iterator

def read_lines(path: str, strip: bool = True, encoding: str = "utf-8") -> Iterator[str]:
    """Stream lines from a text log file."""
    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            yield line.strip() if strip else line

def head(path: str, n: int = 5, encoding: str = "utf-8") -> list[str]:
    """Return first N lines for quick inspection."""
    out: list[str] = []
    for i, line in enumerate(read_lines(path, strip=True, encoding=encoding)):
        out.append(line)
        if i + 1 >= n:
            break
    return out