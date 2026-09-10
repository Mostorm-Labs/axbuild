"""Typed AxBuild errors."""


class AxBuildError(RuntimeError):
    """Base error for expected AxBuild failures."""


class ContractError(AxBuildError):
    """A lock, index, or provider contract is invalid."""


class IntegrityError(AxBuildError):
    """Trusted bytes or materialized content failed integrity validation."""


class OfflineError(AxBuildError):
    """Resolution requires data that is unavailable in offline mode."""


class TransportError(AxBuildError):
    """Release transport failed."""
