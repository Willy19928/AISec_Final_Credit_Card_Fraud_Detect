from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SYNCED_DOCUMENTS = [
    (REPO_ROOT / "DATA_CARD.md", REPO_ROOT / "artifacts" / "DATA_CARD.md"),
    (REPO_ROOT / "MODEL_CARD.md", REPO_ROOT / "artifacts" / "MODEL_CARD.md"),
]


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def main() -> None:
    failures = []
    for root_copy, artifact_copy in SYNCED_DOCUMENTS:
        if not root_copy.exists():
            failures.append(f"missing root document: {root_copy.relative_to(REPO_ROOT)}")
            continue
        if not artifact_copy.exists():
            failures.append(
                f"missing artifact document: {artifact_copy.relative_to(REPO_ROOT)}"
            )
            continue
        if normalized_text(root_copy) != normalized_text(artifact_copy):
            failures.append(
                "document mismatch: "
                f"{root_copy.relative_to(REPO_ROOT)} and "
                f"{artifact_copy.relative_to(REPO_ROOT)}"
            )

    if failures:
        raise SystemExit("\n".join(failures))
    print("Root and artifact documents are synchronized.")


if __name__ == "__main__":
    main()
