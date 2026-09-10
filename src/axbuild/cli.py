"""AxBuild command-line entry points."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .contracts import load_release_index, load_sdk_lock
from .errors import AxBuildError


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="axbuild", description="AxBuild dependency-supply utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_lock = subparsers.add_parser("validate-lock", help="Validate an AxBuild SDK lock")
    validate_lock.add_argument("path", type=Path)

    validate_index = subparsers.add_parser("validate-index", help="Validate an AxBuild release index")
    validate_index.add_argument("path", type=Path)
    return parser


def _handle_validate_lock(path: Path) -> dict[str, object]:
    ref = load_sdk_lock(path)
    return {
        "format": "axbuild-sdk-lock-v1",
        "family": ref.family,
        "repository": ref.repository,
        "releaseTag": ref.release_tag,
        "releaseSetId": ref.identity,
        "indexAsset": ref.asset,
        "indexSha256": ref.sha256,
    }


def _handle_validate_index(path: Path) -> dict[str, object]:
    index = load_release_index(path)
    return {
        "format": "axbuild-release-index-v1",
        "family": index.family,
        "releaseSetId": index.release_set_id,
        "artifactCount": len(index.artifacts),
    }


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate-lock":
            payload = _handle_validate_lock(args.path)
        elif args.command == "validate-index":
            payload = _handle_validate_index(args.path)
        else:  # argparse keeps this unreachable, but preserve fail-closed behavior.
            parser.error(f"unsupported command: {args.command}")
            return 2
    except (AxBuildError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0
