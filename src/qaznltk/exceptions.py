"""Custom exceptions for the qaznltk package."""


class QazNLTKError(Exception):
    """Base exception for all package-specific errors."""


class InvalidInputError(QazNLTKError):
    """Raised when the provided input is invalid."""


class ResourceLoadError(QazNLTKError):
    """Raised when a required resource (URL/file) cannot be loaded."""


class UnsupportedFormatError(QazNLTKError):
    """Raised when a given input format is not supported."""