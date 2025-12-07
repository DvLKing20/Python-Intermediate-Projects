import settings

class DrawMap:

    def __init__(self,surface):
        self.game_surface = surface


    def draw_map(self):
            settings.camera_x = settings.FIXED_WORLD_WIDTH - settings.TARGET_SCREENWIDTH // 2
            settings.camera_y = settings.FIXED_WORLD_HEIGHT - settings.TARGET_SCREENHEIGHT // 2
            # Clamp player inside world boundaries
            settings.camera_x = max(0, min(settings.camera_x, settings.MAPWIDTH - settings.TARGET_SCREENWIDTH))
            settings.camera_y = max(0, min(settings.camera_y, settings.MAPHEIGHT - settings.TARGET_SCREENHEIGHT))
            for layer in settings.MAP.layers:
                if hasattr(layer, "tiles"):
                    for x, y, tile in layer.tiles():
                        world_x = x * settings.MAP.tilewidth
                        world_y = y * settings.MAP.tileheight
                        screen_x = world_x - settings.camera_x
                        screen_y = world_y - settings.camera_y
                        # skipping drawing tiles that drift off the screen
                        if screen_x < -tile.width:
                            continue
                        if screen_y < -tile.height:
                            continue
                        if settings.TARGET_SCREENWIDTH < screen_x:
                            continue
                        if settings.TARGET_SCREENHEIGHT < screen_y:
                            continue
                        self.game_surface.blit(tile, (screen_x, screen_y))

