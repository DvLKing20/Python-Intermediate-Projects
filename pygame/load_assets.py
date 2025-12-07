import os
from pathlib import Path
import pygame



class LoadAssets:
    def __init__(self,directory="",path="",patterns=None,filetype=None):
      """directory is must it will give you every sprite you want to load
         filetype if you want only specific type of file
         patterns is a must like what distinct your files the other ones pass a tuple of strings
         path is optional it defaults to 'the current working path' if not given
         """
      self.dir = Path(os.path.join(path,directory))
      self.directory = directory
      self.patterns = patterns
      self.path = path
      self.filetype = filetype
      #all player animations dir
      self.player_animations = []
      #player animations
      self.player_idle = []
      self.player_idle_up = []
      self.player_idle_down = []
      self.player_idle_left = []
      self.player_idle_right = []
      self.player_up = []
      self.player_down = []
      self.player_left = []
      self.player_right = []


    def load_player_animations(self):
        for i,filename in enumerate(os.listdir(self.dir)):
            if self.filetype:
               if filename.endswith(self.filetype):
                   self.player_animations.append(os.path.join(self.directory,filename))

        for i in range(1,len(self.player_animations)+1):
            for sprite_name in self.player_animations:
                if f"{self.patterns[0]}{i}" in sprite_name:
                    self.player_idle.append(pygame.image.load(sprite_name))
                if f"{self.patterns[1]}{i}" in sprite_name:
                    self.player_up.append(pygame.image.load(sprite_name))
                if f"{self.patterns[2]}{i}" in sprite_name:
                    self.player_down.append(pygame.image.load(sprite_name))
                if f"{self.patterns[3]}{i}" in sprite_name:
                    self.player_left.append(pygame.image.load(sprite_name))
                if f"{self.patterns[4]}{i}" in sprite_name:
                    self.player_right.append(pygame.image.load(sprite_name))
                # if f"{self.patterns[5]}{i}" in sprite_name:
                #     self.player_down.append(pygame.image.load(sprite_name))





if __name__ == "__main__":
    load_assets = LoadAssets()

