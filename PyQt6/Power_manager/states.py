from enum import Enum, auto

class ScanMode(Enum):
      SCAN = auto()
      STOP = auto()

class RenameState(Enum):
      PREVIEW = auto()
      APPLY = auto()
      CANCEL = auto()

class UndoState(Enum):
      UNDO = auto()
      REDO = auto()

class CreateState:
      class ModeState(Enum):
        SIMPLE = auto()
        CUSTOM = auto()

      class ButtonState(Enum):
            CREATE = auto()
            CANCEL = auto()
            PREVIEW = auto()

class CopyState:
    class ButtonState(Enum):
          COPY = auto()
          PREVIEW = auto()
          CANCEL = auto()