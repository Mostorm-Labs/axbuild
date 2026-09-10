"""AxBuild command-line entry points."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .contracts import load_release_index, load_sdk_lock
from .errors import AxBuildError
from .seed import build_nearcast_airplay_seed


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="axbuild", description="AxBuild dependency-supply utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_lock = subparsers.add_parser("validate-lock", help="Validate an AxBuild SDK lock")
    validate_lock.add_argument("path", type=Path)

    validate_index = subparsers.add_parser("validate-index", help="Validate an AxBuild release index")
    validate_index.add_argument("path", type=Path)

    build_seed = subparsers.add_parser(
        "build-nearcast-airplay-seed",
        help="Build a local NearCast AirPlay seed candidate",
    )
    build_seed.add_argument("source_root", type=Path)
    build_seed.add_argument("output_dir", type=Path)
    build_seed.add_argument("--repository", default="Mostorm-Labs/axbuild")
    build_seed.add_argument("--release-tag")
    build_seed.add_argument("--release-set-id")
    build_seed.add_argument("--build-inputs", type=Path)
    build_seed.add_argument("--components", type=Path)
    build_seed.add_argument("--notices", type=Path)
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


def _load_optional_json(path: Path | None) -> object | None:
    if path is None:
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AxBuildError(f"invalid JSON input: {path}: {exc}") from exc
    return value


def _handle_build_seed(args: argparse.Namespace) -> dict[str, object]:
    inputs = _load_optional_json(args.build_inputs)
    components = _load_optional_json(args.components)
    if inputs is not None and not isinstance(inputs, dict):
        raise AxBuildError("--build-inputs must contain a JSON object")
    if components is not None and not isinstance(components, list):
        raise AxBuildError("--components must contain a JSON array")
    notices = None
    if args.notices is not None:
        try:
            notices = args.notices.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise AxBuildError(f"cannot read notices file: {args.notices}: {exc}") from exc
    result = build_nearcast_airplay_seed(
        args.source_root,
        args.output_dir,
        repository=args.repository,
        release_tag=args.release_tag,
        release_set_id=args.release_set_id,
        build_inputs=inputs,
        components=components,
        notices=notices,
    )
    return {
        "format": "axbuild-nearcast-airplay-seed-v1",
        "family": result.family,
        "releaseSetId": result.release_set_id,
        "releaseTag": result.release_tag,
        "artifactIdentity": result.artifact_identity,
        "artifactSha256": result.artifact_sha256,
        "indexSha256": result.index_sha256,
        "archive": str(result.archive_path),
        "index": str(result.index_path),
        "provenance": str(result.provenance_path),
        "lock": str(result.lock_path),
    }


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate-lock":
            payload = _handle_validate_lock(args.path)
        elif args.command == "validate-index":
            payload = _handle_validate_index(args.path)
        elif args.command == "build-nearcast-airplay-seed":
            payload = _handle_build_seed(args)
        else:  # argparse keeps this unreachable, but preserve fail-closed behavior.
            parser.error(f"unsupported command: {args.command}")
            return 2
    except (AxBuildError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0
