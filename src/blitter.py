from src.config import SPRITE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, SHEET_SIZE
import numpy as np

class Blitter:
    def __init__(self, vram_objs):
        self.tiles      = vram_objs.tiles
        self.sprites    = vram_objs.sprites

    def gen_scene(self, scene):
        num_tiles       = SHEET_SIZE // TILE_SIZE
        tile_pool       = (
                           self.tiles.data.reshape(num_tiles, TILE_SIZE,
                                                   num_tiles, TILE_SIZE)
                                          .transpose(0, 2, 1, 3)
                                          .reshape(-1, TILE_SIZE, TILE_SIZE)
                          )
        frame_buffer    = (
                           tile_pool[scene.tile_map].transpose(0, 2, 1, 3)
                                                    .reshape(SCREEN_HEIGHT,
                                                             SCREEN_WIDTH)
                                                    .copy()
                          )
        for sprite in scene.sprites:
            sprite_data = self.sprites[sprite['id']].reshape(SPRITE_SIZE,
                                                             SPRITE_SIZE)
            if sprite['flip_h']:
                sprite_data = np.fliplr(sprite_data)
            if sprite['flip_v']:
                sprite_data = np.flipud(sprite_data)
            if 0 != sprite['rotation']:
                k           = -(sprite['rotation'] // 90)
                sprite_data = np.rot90(sprite_data, k)

            col = sprite['x']
            row = sprite['y']
            fb_row_start   = max(0, row)
            fb_row_stop    = min(SCREEN_HEIGHT, fb_row_start + SPRITE_SIZE)
            fb_col_start   = max(0, col)
            fb_col_stop    = min(SCREEN_HEIGHT, fb_col_start + SPRITE_SIZE)

            if fb_row_start >= fb_row_stop or fb_col_start >= fb_col_stop:
                continue

            sprite_row_start    = fb_row_start - row
            sprite_row_stop     = fb_row_stop - row
            sprite_col_start    = fb_col_start - col
            sprite_col_stop     = fb_col_stop - col

            sprite_chunk        = sprite_data[sprite_row_start:sprite_row_stop,
                                              sprite_col_start:sprite_col_stop]
            fb_chunk            = frame_buffer[fb_row_start:fb_row_stop,
                                               fb_col_start:fb_col_stop]
            bitmask             = (scene.transparent_index != sprite_chunk)
            fb_chunk[bitmask]   = sprite_chunk[bitmask]
        return frame_buffer



