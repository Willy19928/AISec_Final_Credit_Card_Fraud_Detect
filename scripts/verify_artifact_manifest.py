import csv
import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "artifacts" / "artifact_manifest.csv"
ARTIFACT_DIR = REPO_ROOT / "artifacts"
TEXT_SUFFIXES = {".csv", ".json", ".md", ".txt"}


def artifact_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES:
        return raw.replace(b"\r\n", b"\n")
    return raw


def sha256_artifact(path: Path) -> str:
    return hashlib.sha256(artifact_bytes(path)).hexdigest()


def acceptable_sizes(path: Path) -> set[int]:
    raw = path.read_bytes()
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return {len(raw)}

    lf = raw.replace(b"\r\n", b"\n")
    crlf = lf.replace(b"\n", b"\r\n")
    return {len(raw), len(lf), len(crlf)}


def normalize_manifest_path(path_text: str) -> Path:
    path = Path(path_text.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"invalid manifest path: {path_text}")
    if not path.parts or path.parts[0] != "artifacts":
        raise ValueError(f"manifest path must stay under artifacts/: {path_text}")
    if path == Path("artifacts/artifact_manifest.csv"):
        raise ValueError("artifact_manifest.csv must not list itself")
    return path


def main() -> None:
    if not MANIFEST_PATH.exists():
        raise SystemExit("artifacts/artifact_manifest.csv is missing")

    failures = []
    manifest_paths = set()
    with MANIFEST_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required_columns = {"path", "size_bytes", "sha256"}
        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise SystemExit("artifact manifest must contain path,size_bytes,sha256")

        for row in reader:
            try:
                relative_path = normalize_manifest_path(row["path"])
            except ValueError as exc:
                failures.append(str(exc))
                continue
            if relative_path in manifest_paths:
                failures.append(f"duplicate manifest entry: {relative_path}")
                continue
            manifest_paths.add(relative_path)
            artifact_path = REPO_ROOT / relative_path
            expected_size = int(row["size_bytes"])
            expected_sha256 = row["sha256"].strip().lower()
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
            actual_sha256 = sha256_artifact(artifact_path)
            if actual_sha256.lower() != expected_sha256:
                failures.append(
                    f"sha256 mismatch: {relative_path} expected {expected_sha256}; "
                    f"actual {actual_sha256}"
                )

    actual_artifacts = {
        path.relative_to(REPO_ROOT)
        for path in ARTIFACT_DIR.rglob("*")
        if path.is_file() and path.resolve() != MANIFEST_PATH.resolve()
    }
    extra_artifacts = sorted(actual_artifacts - manifest_paths)
    for relative_path in extra_artifacts:
        failures.append(f"unlisted artifact: {relative_path}")

    if failures:
        raise SystemExit("\n".join(failures))
    print("Artifact manifest verified.")


if __name__ == "__main__":
    main()
