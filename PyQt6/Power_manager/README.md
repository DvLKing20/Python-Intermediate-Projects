# PowerManager

PowerManager is a multi-threaded desktop file management application built with Python and PyQt6.  
It provides advanced tools for scanning, renaming, creating, and copying files and directories while keeping the UI fully responsive.

The project is designed with a clean separation between UI, managers, jobs, and workers, making it scalable and safe for long-running filesystem operations.

---

## Features

### Scan
- Recursive directory scanning
- File, folder, and subfolder selection
- Extension-based filtering
- Preview results before applying
- Cancel scan at any time without freezing the UI

### Rename
- Prefix, suffix, sequence, and extension renaming
- Case transformations (capitalize, uppercase, lowercase, title case)
- Live preview mode
- Apply / cancel support
- Undo and redo functionality
- Recursive renaming
- Collision-safe operations

### Create
- Bulk file or folder creation
- Simple and custom modes
- Depth-controlled directory generation
- Preview before creation
- Cancelable operations

### Copy
- Normal copy
- Multiple copy with auto-numbering
- Incremental copy (new or modified files only)
- Collision handling (skip, overwrite, auto-rename)
- Preview before apply
- Cancelable copy operations

---

## Architecture

The project follows a layered architecture:

- UI Layer  
  PyQt6 widgets responsible only for presentation.

- Manager Layer  
  Handles UI state, validation, and user actions.

- Job Layer  
  Manages threads and worker lifecycles.

- Worker Layer  
  Performs filesystem operations inside QObject instances running in QThread.

- State Layer  
  Explicit state machines control scan, rename, create, copy, and undo behavior.

This structure keeps logic organized and prevents UI blocking.

---

## Threading Model

- Uses Qt-recommended QObject + QThread
- Workers moved to threads using moveToThread
- Communication via Qt signals and slots
- Cooperative cancellation using running flags
- Automatic cleanup with deleteLater

The UI remains responsive during all operations.

---

## Tech Stack

- Python 3
- PyQt6
- Qt signals & slots
- QThread-based concurrency
- pathlib, os, shutil

---

## How to Run

`bash
pip install PyQt6
python UI.py