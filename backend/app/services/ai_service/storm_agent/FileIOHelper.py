import json
from os import PathLike

from fs.memoryfs import MemoryFS


# STORM file writing util method does not have utf-8 encoding as well as memory fs requires different code for IO interaction
# Therefore monkey-patch is needed to prevent from crashing when in writing slovak language
class FileIOHelper:
    def __init__(self, memory_fs: MemoryFS) -> None:
        self.memory_fs = memory_fs

    def write_utf8(
        self, s: str, path: int | str | bytes | PathLike[str] | PathLike[bytes]
    ) -> None:
        with self.memory_fs.open(path, "w", encoding="utf-8") as f:
            f.write(s)

    def read_utf8(
        self, path: int | str | bytes | PathLike[str] | PathLike[bytes]
    ) -> str:
        if not self.memory_fs.exists(path):
            raise FileNotFoundError(f"No such file in MemoryFS: '{path}'")
        with self.memory_fs.open(path, "r", encoding="utf-8") as f:
            return f.read()

    def dump_json_memory(self, obj, file_name: str) -> None:  # noqa: ANN001, ARG
        with self.memory_fs.open(file_name, "w", encoding="utf-8") as fw:
            json.dump(obj, fw, default=self.handle_non_serializable)

    def handle_non_serializable(obj) -> str:  # noqa: ANN001, ARG
        return "non-serializable contents"  # mark the non-serializable part

    def load_json_memory(self, file_name: str):  # noqa: ANN201, ARG
        if not self.memory_fs.exists(file_name):
            raise FileNotFoundError(f"No such file in MemoryFS: '{file_name}'")
        with self.memory_fs.open(file_name, "r", encoding="utf-8") as fr:
            return json.load(fr)
