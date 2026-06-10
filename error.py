
class MapError(Exception):
    """Raised when the map contains invalid or inconsistent data."""


class ConnectionError(Exception):
    """Raised when a connection definition is invalid or duplicates exist."""


class HubError(Exception):
    """Raised for errors related to hub definitions and validation."""


class MetadataError(Exception):
    """Raised when metadata values are missing, malformed or invalid.

    Parameters
    ----------
    message : str, optional
        Human readable error message, by default "zone=<type>,
        color=<value>, max_drones=<number>".
    """

    def __init__(
            self,
            message: str = "zone=<type>, color=<value>, max_drones=<number>"
            ) -> None:
        super().__init__(message)
