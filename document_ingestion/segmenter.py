"""NLP utilities to segment text into change entries."""

import re
from typing import Iterable, List


class TextSegmenter:
    """Segment raw text into individual change entries."""

    bullet_regex = re.compile(r"^[\s\-\*\u2022]\s*")

    def segment(self, text: str) -> List[str]:
        lines = text.splitlines()
        entries: List[str] = []
        buffer: List[str] = []

        def flush():
            if buffer:
                entries.append(" ".join(buffer).strip())
                buffer.clear()

        for line in lines:
            if self.bullet_regex.match(line):
                flush()
                buffer.append(self.bullet_regex.sub("", line).strip())
            elif line.strip() == "":
                flush()
            else:
                buffer.append(line.strip())
        flush()
        return [e for e in entries if e]
