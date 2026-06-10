from src.config import *
from src.virtualvram import VirtualVRAM
from src.sceneparser import SceneParser
import numpy as np
from numpy.typing import ArrayLike, NDArray

"""
file:   blitter.py
author: ALESSANDRO QUERENGHI
id:     IN2300001

This files contains the class that generates the scene (applies tiles and
sprites)
"""

class Blitter:
    """
    A Blitter loads sprites and tiles and applies them to the scene
    
    Attributes
    ----------
    tiles : Tiles
        The tiles
    sprites : Sprites
        The sprites

    Methods
    -------
    gen_scene(scene: SceneParser)
        From the given scene, applies the tiles and sprites according to the
        scene and returns the 'frame_buffer' that represents the scene.
    """
    def __init__(self, vram_objs: VirtualVRAM):
        """
        Parameters
        ----------
        vram_objs : VirtualVRAM
            The VirtualVRAM object containing tiles and sprites
        """
        self.tiles      = vram_objs.tiles
        self.sprites    = vram_objs.sprites

    def gen_scene(self, scene: SceneParser) -> NDArray[np.uint8]:
        """
        Generates the scene

        Applies tiles to the background of the scene 'scene' and applies the
        sprites where indicated

        Parameters
        ----------
        scene : SceneParser
            The scene object
        """
        num_tiles       = SHEET_SIZE // TILE_SIZE
        # Reshape the tiles into 4D array
        # tiles[0, 0, 0, :] is the first row of the first tile
        # tiles[0, 0, :, :] is the first row of the first 'num_tiles'
        # tiles[0, :, 0, :] is the first tile
        tile_pool       = (self.tiles.data.reshape(num_tiles, TILE_SIZE,
                                                   num_tiles, TILE_SIZE)
        # change order of axis
        # tiles[0, 0, :, :] is the first tile now
                                          .transpose(0, 2, 1, 3)
        # Reshape in a 3D list of tiles
                                          .reshape(-1, TILE_SIZE, TILE_SIZE))

        # Apply the tiles to the scene.
        # Now the scene is 4D and dimsn contain: 
        # [scene_height, SCENE_WIDTH, TILE_SIZE, TILE_SIZE]
        # Transposed axes to obtain 
        # [SCENE_HEIGHT, TILE_SIZE, SCENE_WIDTH, TILE_SIZE]
        frame_buffer    = (tile_pool[scene.tile_map].transpose(0, 2, 1, 3)
        # reshape to obtain a 2D image
                                                    .reshape(SCREEN_HEIGHT,
                                                             SCREEN_WIDTH)
                                                    .copy())
        # now applying sprites
        for sprite in scene.sprites:
            sprite_data = self.sprites[sprite['id']]
            # apply flips and rotations
            if sprite['flip_h']:
                sprite_data = np.fliplr(sprite_data)
            if sprite['flip_v']:
                sprite_data = np.flipud(sprite_data)
            if 0 != sprite['rotation']:
                k           = -(sprite['rotation'] // 90)
                sprite_data = np.rot90(sprite_data, k)
            # computing where the sprite will be positioned
            col = sprite['x']
            row = sprite['y']
            # if the sprite is positioned partially offscreen, compute its
            # position on the scene
            fb_row_start   = max(0, row)
            fb_row_stop    = min(SCREEN_HEIGHT, fb_row_start + SPRITE_SIZE)
            fb_col_start   = max(0, col)
            fb_col_stop    = min(SCREEN_WIDTH, fb_col_start + SPRITE_SIZE)
            # if completely offscren don't apply it
            if fb_row_start >= fb_row_stop or fb_col_start >= fb_col_stop:
                continue
            # computing how much of the sprite is visible
            sprite_row_start    = fb_row_start - row
            sprite_row_stop     = fb_row_stop - row
            sprite_col_start    = fb_col_start - col
            sprite_col_stop     = fb_col_stop - col
            # the visible part of the sprite
            sprite_chunk        = sprite_data[sprite_row_start:sprite_row_stop,
                                              sprite_col_start:sprite_col_stop]
            # the part of the scene that will hold the sprite
            fb_chunk            = frame_buffer[fb_row_start:fb_row_stop,
                                               fb_col_start:fb_col_stop]
            # compute transparency mask
            bitmask             = (scene.transparent_index != sprite_chunk)
            # apply sprite to scene and remove transparent bits
            fb_chunk[bitmask]   = sprite_chunk[bitmask]
        return frame_buffer

