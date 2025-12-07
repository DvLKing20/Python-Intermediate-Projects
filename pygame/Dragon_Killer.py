import settings
from load_assets import LoadAssets
from player import Player
from my_map import DrawMap
import pygame
pygame.init()


class  DragonKiller:
    def __init__(self):
        #MYMODULE FOR ASSETS
        self.assets = LoadAssets(directory="player", patterns=("_idle","_w","_s","_a","_d"),filetype=("png","jpg"))
        self.player_assets = self.assets.load_player_animations()
        #WINDOW AND TITLE
        pygame.display.set_caption(settings.SCREEN_TITLE)
        self.window = settings.PYGAME_WINDOW
        self.game_surface = settings.PYGAME_SURFACE
        self.MAP = settings.MAP
        #classes for player and draw_map
        self.player = Player(self.assets,self.game_surface)
        self.draw_map = DrawMap(self.game_surface)
        self.clock = pygame.time.Clock()
    def draw_loop(self):

        while settings.RUN_GAME:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   settings.RUN_GAME = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                 break
            scaled_surface = pygame.transform.scale(self.game_surface, (settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))
            self.game_surface.fill((0,0,0))
            self.draw_map.draw_map()
            self.player.draw_player(keys)
            self.window.blit(scaled_surface, (0, 0))
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = DragonKiller()
    game.draw_loop()