"""Document ingestion package for vendor release automation."""

from .watcher import FolderWatcher
from .parser import DocumentParser
from .segmenter import TextSegmenter

__all__ = ["FolderWatcher", "DocumentParser", "TextSegmenter"]
