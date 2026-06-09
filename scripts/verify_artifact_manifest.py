import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "artifacts" / "artifact_manifest.csv"
TEXT_SUFFIXES = {".csv", ".json", ".md", ".txt"}


def acceptable_sizes(path: Path) -> set[int]:
    raw = path.read_bytes()
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return {len(raw)}

    lf = raw.replace(b"\r\n", b"\n")
    crlf = lf.replace(b"\n", b"\r\n")
    return {len(raw), len(lf), len(crlf)}


def main() -> None:
    if not MANIFEST_PATH.exists():
        raise SystemExit("artifacts/artifact_manifest.csv is missing")

    failures = []
    with MANIFEST_PATH.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            relative_path = Path(row["path"].replace("\\", "/"))
            artifact_path = REPO_ROOT / relative_path
            expected_size = int(row["size_bytes"])
            if not artifact_path.exists():
                failures.append(f"missing: {relative_path}")
                continue

            sizes = acceptable_sizes(artifact_path)
            if expected_size not in sizes:
                actual_sizes = ", ".join(str(size) for size in sorted(sizes))
                failures.append(
                    f"size mismatch: {relative_path} expected {expected_size}; "
                    f"acceptable checkout sizes: {actual_sizes}"
                )

    if failures:
        raise SystemExit("\n".join(failures))
    print("Artifact manifest verified.")


if __name__ == "__main__":
    main()
