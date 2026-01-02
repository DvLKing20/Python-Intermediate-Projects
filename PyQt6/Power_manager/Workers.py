import os,shutil
from pathlib import Path
from PyQt6.QtCore import pyqtSignal, QObject

from states import UndoState, CreateState


class ScanWorker(QObject):
    """Scans directories and collects file metadata."""
    finished = pyqtSignal(int,int,int,list,list)

    def __init__(self, path: str, chk_status: list, extension: str) -> None:
        super().__init__()
        self.running = True
        self.Path = path
        self.extension = extension

        (self.files_status,
        self.dirs_status,
        self.subdirs_status,
        self.preview_status,
        self.hidden_status,) = chk_status

        self.files = 0
        self.dirs = 0
        self.subdirs = 0

        self.filenames = []
        self.dirnames = []

    def run_scan(self):
        """Start directory scan in worker thread."""
        path = self.Path
        try:
          with os.scandir(path) as entries:
             for entry in entries:
                if not self.running:
                   break

                if entry.is_file() and self.files_status and not self.extension:
                    self.files += 1
                    if not self.preview_status:
                       self.filenames.append(entry.name)
                elif entry.is_file() and self.files_status and self.extension:
                     ext = self.extension.lstrip(".")
                     if entry.name.endswith("."+self.extension):
                         self.files += 1
                         if not self.preview_status:
                            self.filenames.append(entry.name)

                if entry.is_dir() and self.dirs_status:
                     self.dirs+=1
                     if not self.preview_status:
                        self.dirnames.append(entry.name)
                     if self.subdirs_status:
                        self.run_subdir_scan(entry.path)

        except OSError as e:
         print(e)

        self.finished.emit(self.dirs,self.files,self.subdirs,self.filenames,self.dirnames)

    def run_subdir_scan(self, path):
        if not self.running:
           return

        try:
          with os.scandir(path) as entries:
             for entry in entries:
                if entry.is_file() and self.files_status and not self.extension:
                    self.files += 1
                    if not self.preview_status:
                       self.filenames.append(entry.name)
                elif entry.is_file() and self.files_status and self.extension:
                     if entry.name.endswith(self.extension):
                         self.files += 1
                         if not self.preview_status:
                            self.filenames.append(entry.name)

                if entry.is_dir() and self.dirs_status:
                     self.subdirs+=1
                     if not self.preview_status:
                        self.dirnames.append(entry.name)
                     if self.subdirs_status:
                        self.run_subdir_scan(entry.path)

        except OSError as e:
         print(e)

    def stop_scan(self):
        """Stop the running operation."""
        self.running = False


class RenameWorker(QObject):
    """Applies batch rename rules to files."""
    finished = pyqtSignal(list,list,list,list,list,list,bool)

    class UndoRedo(QObject):
        """Undo rename worker."""
        finished = pyqtSignal(list,list,list,list,object)

        def __init__(self, file_stack: tuple, dir_stack: tuple, state: object) -> None:
            super().__init__()
            self.file_stack = file_stack
            self.dir_stack = dir_stack
            self.state = state
            self.old_file = []
            self.new_file = []
            self.old_dir = []
            self.new_dir = []

        def undo(self):
           if self.file_stack:
            for old,new in self.file_stack:
                new.rename(old)
                self.old_file.append(old.name)
                self.new_file.append(new.name)
           if self.dir_stack:
              for old,new in self.dir_stack:
                  new.rename(old)
                  self.old_dir.append(old.name)
                  self.new_dir.append(new.name)

        def redo(self):
            if self.file_stack:
                for old, new in self.file_stack:
                    old.rename(new)
                    self.old_file.append(new.name)
                    self.new_file.append(old.name)
            if self.dir_stack:
                for old, new in self.dir_stack:
                    old.rename(new)
                    self.old_dir.append(new.name)
                    self.new_dir.append(old.name)

        def main(self):
            match self.state:
                case UndoState.UNDO:
                     self.undo()
                     self.state = UndoState.REDO
                case UndoState.REDO:
                     self.redo()
                     self.state = UndoState.UNDO

            self.finished.emit(self.old_file,self.new_file,self.old_dir,self.new_dir,self.state)

    def __init__(self, path: str, chk_status: tuple, text: str, apply: bool) -> None:
        super().__init__()
        self.apply = apply
        self.running = True
        self.Path = path
        self.text = text

        (   self.chk_scope_status,
            self.chk_rename_status,
            self.cases
        ) = chk_status

        (self.file,
         self.folder,
         self.subdirs,
         self.live_preview,
         self.preview) = self.chk_rename_status

        self.source_files = []
        self.target_files = []
        self.source_dirs = []
        self.target_dirs = []
        self.file_stack = []
        self.dir_stack = []

    def run_rename(self):
        path = self.Path
        match self.cases:
            case (True, False, False, False):
                 transform = str.capitalize
            case (False, True, False, False):
                 transform = str.upper
            case (False, False, True, False):
                 transform = str.lower
            case (False, False, False, True):
                 transform = str.title
            case _:
                 transform = str

        match self.chk_scope_status:
              case (True, False, False, False) | (False, True, False, False):
                   self.prefix_suffix_sequence(path,transform)
              case (False, False, True, False):
                   self.number_sequence(path,transform)
              case (False, False, False, True):
                   self.extension_sequence(path,transform)

        self.finished.emit(self.source_files,self.target_files,self.source_dirs,self.target_dirs,
                           self.file_stack,self.dir_stack,self.apply)

    def extension_sequence(self,path,transform):
        try:
              entries = list(os.scandir(path))
              for entry in entries:
                 if not self.running:
                     break
                 if entry.is_file() and  self.file:
                    base,ext = os.path.splitext(entry.name)

                    old_path = Path(entry.path)
                    new_name = transform(base) + "." + self.text.lstrip('.')
                    new_path = old_path.with_name(new_name)

                    self.source_files.append(entry.name)
                    self.target_files.append(new_name)

                    if self.apply:
                       old_path.rename(new_path)
                       self.file_stack.append((old_path,new_path))

                 if entry.is_dir() and self.subdirs:
                    self.extension_sequence(entry.path,transform)

        except OSError as e:
            print(e)

    def prefix_suffix_sequence(self,path,transform):
        try:
              entries = list(os.scandir(path))
              for entry in entries:
                 if not self.running:
                     break
                 if entry.is_file() and  self.file:
                    base,ext = os.path.splitext(entry.name)

                    old_path = Path(entry.path)
                    new_name = (transform(f"{self.text}{base}") + ext
                                if self.chk_scope_status[1]
                                else transform(f"{base}{self.text}") + ext)
                    new_path = old_path.with_name(new_name)

                    self.source_files.append(entry.name)
                    self.target_files.append(new_name)

                    if self.apply:
                       old_path.rename(new_path)
                       self.file_stack.append((old_path,new_path))

                 if entry.is_dir():
                    old_path = Path(entry.path)
                    next_path = old_path
                    if self.folder:

                       new_name = (transform(f"{self.text}{entry.name}")
                                if self.chk_scope_status[1]
                                else transform(f"{entry.name}{self.text}"))
                       new_path = old_path.with_name(new_name)

                       self.source_dirs.append(entry.name)
                       self.target_dirs.append(new_name)

                       if self.apply:
                          old_path.rename(new_path)
                          self.dir_stack.append((old_path,new_path))
                          next_path = new_path

                    if self.subdirs:
                          self.prefix_suffix_sequence(next_path,transform)


        except OSError as e:
            print(e)

    def number_sequence(self,path,transform):
        count = 1
        padding = 3
        next_padding = 1000
        try:
                entries = list(os.scandir(path))
                for entry in entries:
                    if not self.running:
                       break
                    if count == next_padding:
                          padding += 1
                          next_padding *= 10
                    renamed = False

                    if entry.is_file() and self.file:
                        renamed = True
                        base, ext = os.path.splitext(entry.name)

                        #New Path
                        old_path = Path(entry.path)
                        new_base = transform(f"{base}_{count:0{padding}d}") + ext
                        new_path = old_path.with_name(new_base)

                        #preview
                        self.source_files.append(entry.name)
                        self.target_files.append(new_base)

                        if self.apply:
                           old_path.rename(new_path)
                           self.file_stack.append((old_path, new_path))


                    if entry.is_dir():
                       old_path = Path(entry.path)
                       next_path = old_path
                       if self.folder:
                          renamed = True
                          #New Path
                          new_base = transform(f"{entry.name}_{count:0{padding}d}")
                          new_path = old_path.with_name(new_base)

                          #preview
                          self.source_dirs.append(entry.name)
                          self.target_dirs.append(new_base)

                          if self.apply:
                             old_path.rename(new_path)
                             self.dir_stack.append((old_path, new_path))
                             next_path = new_path

                       if self.subdirs:
                          self.number_sequence(next_path,transform)

                    if renamed:
                       count+=1
        except OSError as e:
                    print(e)

    def stop_rename(self):
        self.running = False

class CreateWorker(QObject):
    finished = pyqtSignal(list,list,object,bool)

    def __init__(self,path,file_name, folder_name, ext, count, mode, state, apply: bool):
        super().__init__()
        self.running = True

        self.path = path
        self.file_name = file_name
        self.folder_name = folder_name
        self.ext = ext
        self.counter = count

        self.mode = mode
        self.state = state
        self.apply = apply

        self.file_stack = []
        self.dir_stack = []

    def run_create(self):
        path = self.path
        match self.mode:
              case CreateState.ModeState.SIMPLE:
                   self.run_simple_mode(path)
              case CreateState.ModeState.CUSTOM:
                   self.run_custom_mode(path)
        self.finished.emit(self.file_stack,self.dir_stack,self.mode,self.apply)

    def run_custom_mode(self,path):
        depth = self.counter["depth"]

        base = Path(path)
        if not self.running:
           return
        if self.file_name:
           for count in range(1,self.counter["file"]+1):
               name = f"{self.file_name}_{count}"
               full_name = name + ("."+self.ext.lstrip(".") if self.ext else "")

               if self.apply:
                  new_path = base / full_name

                  if new_path.exists():
                     continue

                  new_path.touch()
               self.file_stack.append(full_name)

        if self.folder_name:
            all_path = []
            for count in range(1, self.counter["folder"] + 1):
                folder_name = f"{self.folder_name}_{count:02d}"

                if self.apply:
                   new_path = base / folder_name

                   if new_path.exists():
                      continue

                   new_path.mkdir(parents=True, exist_ok=False)

                   if depth > 0:
                      all_path.append(new_path)

                self.dir_stack.append(folder_name)
            if depth > 0:
               self.counter["depth"] -= 1
               for path in all_path:
                   self.run_custom_mode(path)


    def run_simple_mode(self, path):
        base_path = Path(path)
        for count in range(1, self.counter + 1):
            if not self.running:
                break
            name = f"{self.file_name}_{count:02d}"
            if self.state[0]:  # FILE MODE
                full_name = name + ("."+self.ext.lstrip(".") if self.ext else "")
                new_path = base_path / full_name
                if self.apply:
                    if new_path.exists():
                        continue
                    new_path.touch()
                self.file_stack.append(full_name)
            else:  # FOLDER MODE
                new_path = base_path / name
                if self.apply:
                    if new_path.exists():
                        continue
                    new_path.mkdir(parents=True, exist_ok=False)
                self.dir_stack.append(name)


class CopyWorker(QObject):
    finished = pyqtSignal(list,list,bool)

    def __init__(self, path, dst_path, scope, copy_mode, collision, count, apply):
        super().__init__()
        self.running = True
        self.src_path = path
        self.dst_path = dst_path
        self.scope = scope
        self.copy_mode = copy_mode
        self.collision = collision
        self.count = count
        self.apply = apply

        self.file_stack = []
        self.dir_stack = []

    def main(self):
        normal,multiple,incremental = self.copy_mode
        path1 = self.src_path
        path2 = self.dst_path

        if normal:
            self.normal_copy(path1,path2)
        elif multiple:
             self.multiple_copy(path1,path2)
        elif incremental:
             self.incremental_copy(path1,path2)

        self.finished.emit(self.file_stack,self.dir_stack,self.apply)


    def incremental_copy(self,path1,path2):
            file, dir, subdir, name = self.scope
            skip, overwrite, auto_rename = self.collision

            src_path = Path(path1)
            dst_path = Path(path2)

            if not src_path.exists():
                return

            for entry in src_path.iterdir():
                if not self.running:
                    break

                dst_entry = dst_path / entry.name

                # ---------- FILES ----------
                if entry.is_file() and file:
                    copy = False

                    if not dst_entry.exists():
                        copy = True
                    else:
                        src_stat = entry.stat()
                        dst_stat = dst_entry.stat()
                        if src_stat.st_size != dst_stat.st_size or src_stat.st_mtime > dst_stat.st_mtime:
                            copy = True

                    if copy and self.apply:
                        if dst_entry.exists() and auto_rename:
                            i = 0
                            while True:
                                candidate = dst_path / f"{entry.stem}_{i:02d}{entry.suffix}"
                                if not candidate.exists():
                                    dst_entry = candidate
                                    break
                                i += 1

                        shutil.copy2(entry, dst_entry)

                    if copy:
                        self.file_stack.append(str(dst_entry))

                # ---------- DIRECTORIES ----------
                if entry.is_dir() and dir:
                    if not dst_entry.exists():
                        if self.apply:
                            dst_entry.mkdir(parents=True, exist_ok=True)
                        self.dir_stack.append(str(dst_entry))

                    if subdir:
                        self.incremental_copy(entry, dst_entry)

    def multiple_copy(self,path1,path2):
        file, dir, subdir,name = self.scope
        skip, overwrite, auto_rename = self.collision

        src_path = Path(path1)
        dst_path = Path(path2)

        for count in range(1,self.count+1):
            if not self.running:
                break

            match self.scope:
                case (True,True,True,False) | (True,True,True,True) if src_path.is_dir():
                     full_path = f"{src_path.name}_{count:02d}"
                     target = dst_path / full_path

                     if self.apply and full_path:
                        if not name:
                           shutil.copytree(src_path,target,dirs_exist_ok=overwrite)
                        else:
                           target.mkdir(parents=True, exist_ok=overwrite) if not target.exists() else None
                           self.normal_copy(src_path,target)
                     self.dir_stack.append(full_path)

                case (True,False,False,False) | (True,False,True,False) | ((True,False,False,True)) | (True,False,True,True):
                     if src_path.is_file():
                        ext,file = src_path.suffix,src_path.stem
                        file_name = dst_path / f"{file}_{count:02d}{ext}"
                        if self.apply and file_name:
                           shutil.copy2(src_path,file_name) if not name else file_name.touch()
                        self.file_stack.append(file_name.name)

                     if subdir and src_path.is_dir():
                       def organize(src_path,dst_path):
                           for entry in src_path.iterdir():
                               if entry.is_file():
                                  target = dst_path / entry.stem
                                  if target.exists() and skip:
                                     continue
                                  if self.apply and not target.exists():
                                     target.mkdir(parents=True, exist_ok=overwrite)
                                  self.dir_stack.append(entry.name)
                                  self.multiple_copy(entry,target)
                               if entry.is_dir():
                                  organize(entry,dst_path)
                       organize(src_path,dst_path)
                       break
                case (False,True,False,False) | (False,True,True,False) | (False,True,True,True) | (False,True,False,True):
                     if dir:
                        target = dst_path / f"{src_path.name}{count:02d}"
                        if self.apply:
                           if target.exists() and skip: continue
                           target.mkdir(parents=True, exist_ok=overwrite)
                           if subdir:
                              def make_folders(src_path,dst_path):
                                  for entry in src_path.iterdir():
                                     if entry.is_dir():
                                        subdirs = dst_path / entry.name
                                        if subdirs.exists() and skip: continue
                                        subdirs.mkdir(parents=True, exist_ok=overwrite)
                                        make_folders(entry,subdirs)
                              make_folders(src_path,target)

                        self.dir_stack.append(target.name)


    def normal_copy(self,path1,path2):
        file, dir, subdir, name = self.scope
        skip, overwrite, auto_rename = self.collision

        src_path = Path(path1)
        dst_path = Path(path2)
        if not src_path.is_dir() or not src_path.exists():
            return
        for entry in src_path.iterdir():
            if not self.running:
               break
            if file and entry.is_file():
               target = dst_path / entry.name
               if self.apply:
                  if target.exists() and skip:
                     continue
                  if target.exists() and auto_rename:
                     count = 0
                     while True:
                         target = dst_path / f"{entry.stem}_{count:02d}{entry.suffix}"
                         if not target.exists():
                            break
                         count += 1
                  (target.touch(exist_ok=overwrite)
                   if name
                   else shutil.copy2(entry, target))
               self.file_stack.append(str(target))
            if subdir and file and entry.is_dir() and not dir:
                next_src = entry
                next_dst = dst_path
                self.normal_copy(next_src, next_dst)

            if dir and entry.is_dir():
               chk_entry = dst_path / entry.name
               target = chk_entry
               if self.apply:
                  if chk_entry.exists() and skip:
                     continue
                  if auto_rename and chk_entry.exists():
                      count = 0
                      while True:
                          target = dst_path / f"{entry.name}_{count:02d}"
                          if not target.exists():
                              break
                          count += 1
                  target.mkdir(parents=True, exist_ok=overwrite)
               self.dir_stack.append(str(target))
               if subdir and target.exists():
                     next_src = entry
                     next_dst = target
                     self.normal_copy(next_src, next_dst)
