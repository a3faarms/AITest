# Vendor Release Document Ingestion

This repository provides an initial module for automating vendor release document analysis. The focus of this iteration is **document ingestion and parsing**.

## Components

- `FolderWatcher` – polls a directory and triggers a callback when new PDF or Word documents are added.
- `DocumentParser` – extracts raw text from PDF (`pdfminer.six`) and Word (`python-docx`) files.
- `TextSegmenter` – splits the extracted text into individual change entries using simple NLP rules.

## Example Usage

```python
from pathlib import Path
from document_ingestion import FolderWatcher, DocumentParser, TextSegmenter

watch_dir = Path("./incoming")
parser = DocumentParser()
segmenter = TextSegmenter()

def handle_file(path: Path):
    text = parser.parse(path)
    entries = segmenter.segment(text)
    print(f"Parsed {len(entries)} entries from {path.name}")
    for entry in entries:
        print("-", entry)

watcher = FolderWatcher(watch_dir, handle_file)
# Run indefinitely: watcher.run_forever()
```

Place documents in the `incoming` directory and run the script. Each new file will be processed and segmented into change entries.

## Testing Instructions

1. Install dependencies:
   ```bash
   pip install watchdog pdfminer.six python-docx
   ```
2. Create an `incoming` folder and place sample PDF/Word files containing bullet lists of changes.
3. Run the example script above or your own script that uses the provided classes.
4. Verify that change entries are printed to the console.

## Next Steps

- Implement classification of change entries (New Feature, Bug Fix, etc.).
- Add embedding and similarity search to map changes to internal modules and test cases.
- Build a web-based UI and conversational assistant for interactive review.
- Integrate with JIRA, Confluence, and GitHub APIs.

These modules are designed to be imported into larger services and can be extended as the project grows.
