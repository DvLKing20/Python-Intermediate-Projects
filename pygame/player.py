import pygame
import settings
from settings import camera_x


class Player:
    W = 0
    S = 0
    A = 0
    D = 0
    idle = 0
    PLAYER_SPEED = 0
    WORLD_SPEED = 1
    def __init__(self,assets,game_surface):
        #PLAYER_RECT
        self.assets = assets
        self.game_surface = game_surface
        self.player_bubble = pygame.Rect(0, 0, 60, 80)
        player_idle = self.assets.player_idle[0]
        self.player_rect = player_idle.get_rect(
            center=(settings.TARGET_SCREENWIDTH // 2, settings.TARGET_SCREENHEIGHT // 2))
        self.player_bubble.center = self.player_rect.center


    def draw_player(self, keys):
            pygame.draw.rect(self.game_surface, 'red', self.player_bubble,1)
            if keys[pygame.K_a]:

                if  self.player_rect.left >= 0:
                    self.player_rect.x -= self.PLAYER_SPEED
                    self.player_bubble.center = self.player_rect.center

                if  settings.camera_x > 0:
                    settings.FIXED_WORLD_WIDTH -= self.WORLD_SPEED

                self.A += 0.15  # animation speed
                if self.A >= len(self.assets.player_left):
                    self.A = 0
                self.game_surface.blit(self.assets.player_left[int(self.A)], self.player_rect)

            elif keys[pygame.K_d]:
                border = settings.MAPWIDTH - settings.TARGET_SCREENWIDTH

                if  self.player_rect.right <= settings.TARGET_SCREENWIDTH:
                    self.player_rect.x += self.PLAYER_SPEED
                    self.player_bubble.center = self.player_rect.center

                if  settings.camera_x < border:
                    settings.FIXED_WORLD_WIDTH += self.WORLD_SPEED

                if  camera_x >= border:
                    self.PLAYER_SPEED = 1

                self.D += 0.15 # animation speed
                if self.D >= len(self.assets.player_right):
                    self.D = 0
                self.game_surface.blit(self.assets.player_right[int(self.D)], self.player_rect)

            elif keys[pygame.K_s]:
                border = settings.MAPHEIGHT - settings.TARGET_SCREENHEIGHT

                if  self.player_rect.bottom < settings.TARGET_SCREENHEIGHT:
                    self.player_rect.y += self.PLAYER_SPEED
                    self.player_bubble.center = self.player_rect.center

                if  settings.camera_y < border:
                    settings.FIXED_WORLD_HEIGHT += self.WORLD_SPEED

                if settings.camera_y >= border:
                    self.PLAYER_SPEED = 1

                self.S += 0.15  # animation speed
                if self.S >= len(self.assets.player_down):
                    self.S = 0
                self.game_surface.blit(self.assets.player_down[int(self.S)], self.player_rect)

            elif keys[pygame.K_w]:
                if  self.player_rect.top > 0:
                    self.player_rect.y -= self.PLAYER_SPEED
                    self.player_bubble.center = self.player_rect.center

                if  settings.camera_y > 0:
                    settings.FIXED_WORLD_HEIGHT -= self.WORLD_SPEED

                self.W += 0.07
                if self.W >= len(self.assets.player_up):
                    self.W = 0
                self.game_surface.blit(self.assets.player_up[int(self.W)], self.player_rect)

            else:
                self.idle += 0.04
                if self.idle >= len(self.assets.player_idle):
                    self.idle = 0
                self.game_surface.blit(self.assets.player_idle[int(self.idle)].convert_alpha(), self.player_rect)

