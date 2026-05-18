
class MapError(Exception):
    ...


class ConnectionError(Exception):
    ...


class HubError(Exception):
    ...


class MetadataError(Exception):
    def __init__(
            self,
            message: str = "zone=<type>, color=<value>, max_drones=<number>"
            ) -> None:
        super().__init__(message)
