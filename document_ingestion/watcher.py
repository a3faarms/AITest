"""Folder monitoring utilities for document ingestion."""

import time
from pathlib import Path
from typing import Callable, Iterable

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError as exc:
    raise ImportError("watchdog package is required: pip install watchdog") from exc


class _Handler(FileSystemEventHandler):
    """Internal handler that triggers callbacks on new files."""

    def __init__(self, callback: Callable[[Path], None], patterns: Iterable[str]):
        self.callback = callback
        self.patterns = tuple(patterns)

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() in self.patterns:
            self.callback(path)


class FolderWatcher:
    """Watch a folder for new documents and invoke callback."""

    def __init__(self, directory: Path, callback: Callable[[Path], None],
                 patterns: Iterable[str] = (".pdf", ".docx")) -> None:
        self.directory = Path(directory)
        self.callback = callback
        self.patterns = patterns
        self.observer = Observer()
        self.handler = _Handler(callback, patterns)

    def start(self) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        self.observer.schedule(self.handler, str(self.directory), recursive=False)
        self.observer.start()

    def run_forever(self) -> None:
        try:
            self.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        self.observer.stop()
        self.observer.join()
