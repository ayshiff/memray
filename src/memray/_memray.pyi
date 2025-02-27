import enum
from pathlib import Path
from types import FrameType
from types import TracebackType
from typing import Any
from typing import Iterable
from typing import Iterator
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from typing import overload

from memray._destination import FileDestination as FileDestination
from memray._destination import SocketDestination as SocketDestination
from memray._metadata import Metadata
from memray._stats import Stats

from . import Destination

PythonStackElement = Tuple[str, str, int]
NativeStackElement = Tuple[str, str, int]
MemorySnapshot = NamedTuple(
    "MemorySnapshot", [("time", int), ("rss", int), ("heap", int)]
)

def set_log_level(level: int) -> None: ...

class AllocationRecord:
    @property
    def address(self) -> int: ...
    @property
    def allocator(self) -> int: ...
    @property
    def n_allocations(self) -> int: ...
    @property
    def size(self) -> int: ...
    @property
    def stack_id(self) -> int: ...
    @property
    def tid(self) -> int: ...
    @property
    def thread_name(self) -> str: ...
    def hybrid_stack_trace(
        self,
        max_stacks: Optional[int] = None,
    ) -> List[Union[PythonStackElement, NativeStackElement]]: ...
    def native_stack_trace(
        self, max_stacks: Optional[int] = None
    ) -> List[NativeStackElement]: ...
    def stack_trace(
        self, max_stacks: Optional[int] = None
    ) -> List[PythonStackElement]: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ge__(self, other: Any) -> Any: ...
    def __gt__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...
    def __le__(self, other: Any) -> Any: ...
    def __lt__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...

class AllocatorType(enum.IntEnum):
    MALLOC: int
    FREE: int
    CALLOC: int
    REALLOC: int
    POSIX_MEMALIGN: int
    ALIGNED_ALLOC: int
    MEMALIGN: int
    VALLOC: int
    PVALLOC: int
    MMAP: int
    MUNMAP: int
    PYMALLOC_MALLOC: int
    PYMALLOC_CALLOC: int
    PYMALLOC_REALLOC: int
    PYMALLOC_FREE: int

def start_thread_trace(frame: FrameType, event: str, arg: Any) -> None: ...

class FileReader:
    @property
    def metadata(self) -> Metadata: ...
    def __init__(
        self, file_name: Union[str, Path], *, report_progress: bool = False
    ) -> None: ...
    def get_allocation_records(self) -> Iterable[AllocationRecord]: ...
    def get_high_watermark_allocation_records(
        self,
        merge_threads: bool = ...,
    ) -> Iterable[AllocationRecord]: ...
    def get_leaked_allocation_records(
        self, merge_threads: bool = ...
    ) -> Iterable[AllocationRecord]: ...
    def get_temporary_allocation_records(
        self, merge_threads: bool = ..., threshold: int = ...
    ) -> Iterable[AllocationRecord]: ...
    def get_memory_snapshots(self) -> Iterable[MemorySnapshot]: ...
    def __enter__(self) -> Any: ...
    def __exit__(
        self,
        exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        exctb: Optional[TracebackType],
    ) -> bool: ...
    @property
    def closed(self) -> bool: ...
    def close(self) -> None: ...

def compute_statistics(
    file_name: Union[str, Path],
    *,
    report_progress: bool = False,
    num_largest: int = 5,
) -> Stats: ...
def dump_all_records(file_name: Union[str, Path]) -> None: ...

class SocketReader:
    def __init__(self, port: int) -> None: ...
    def __enter__(self) -> "SocketReader": ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> Any: ...
    def get_current_snapshot(
        self, *, merge_threads: bool
    ) -> Iterator[AllocationRecord]: ...
    @property
    def command_line(self) -> Optional[str]: ...
    @property
    def is_active(self) -> bool: ...
    @property
    def pid(self) -> Optional[int]: ...
    @property
    def has_native_traces(self) -> bool: ...

class Tracker:
    @property
    def reader(self) -> FileReader: ...
    @overload
    def __init__(
        self,
        file_name: Union[Path, str],
        *,
        native_traces: bool = ...,
        memory_interval_ms: int = ...,
        follow_fork: bool = ...,
        trace_python_allocators: bool = ...,
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        destination: Destination,
        native_traces: bool = ...,
        memory_interval_ms: int = ...,
        follow_fork: bool = ...,
        trace_python_allocators: bool = ...,
    ) -> None: ...
    def __enter__(self) -> Any: ...
    def __exit__(
        self,
        exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        exctb: Optional[TracebackType],
    ) -> bool: ...

def greenlet_trace(event: str, args: Any) -> None: ...

class PymallocDomain(enum.IntEnum):
    PYMALLOC_RAW: int
    PYMALLOC_MEM: int
    PYMALLOC_OBJECT: int

def size_fmt(num: int, suffix: str = "B") -> str: ...

class SymbolicSupport(enum.IntEnum):
    NONE: int
    FUNCTION_NAME_ONLY: int
    TOTAL: int

def get_symbolic_support() -> SymbolicSupport: ...
