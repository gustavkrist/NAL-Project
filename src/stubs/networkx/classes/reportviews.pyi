from typing import Generator


class DegreeView:
    def __iter__(self) -> Generator[tuple[int | str, int], None, None]: ...
