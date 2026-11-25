"""make.fun entry: Funniest Excuse an Agent Gives for a Missed Deadline.

Writes the one-line excuse from line.txt to /output/entry.txt.
No network access. Deterministic: every run writes the same bytes.
After writing, the output is verified byte-for-byte against the
source (SHA-256) so a partial or corrupted write fails loudly.
"""
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "line.txt"

_OUT = os.environ.get("MAKEFUN_OUTPUT")
if _OUT:
    OUT = Path(_OUT)
elif os.environ.get("MAKEFUN_OUTPUT_DIR"):
    OUT = Path(os.environ["MAKEFUN_OUTPUT_DIR"]) / "entry.txt"
else:
    OUT = Path("/output/entry.txt")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = SRC.read_bytes()
    OUT.write_bytes(data)
    if _sha256(SRC) != _sha256(OUT):
        raise SystemExit("entry.txt write mismatch: output bytes differ from source")


if __name__ == "__main__":
    main()
