import pytmx
from constants import *


class Map:
    """
    Loads map from tsx file
    """

    def __init__(self, file):
        self.tiled_map_data = pytmx.load_pygame(f'data/{file}')

    def full_map(self):
        """Loads map"""
        full_map = pygame.Surface(MAP_SIZE)
        for layer in self.tiled_map_data.visible_layers:
            if type(layer) == pytmx.TiledTileLayer:
                for x, y, gid in layer:
                    tile = self.tiled_map_data.get_tile_image_by_gid(gid)
                    if tile:
                        full_map.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
        return full_map
