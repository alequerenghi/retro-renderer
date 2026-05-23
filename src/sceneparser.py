from src.config import *
import numpy as np
import json
from numpy.typing import NDArray, ArrayLike

"""
file:   sceneparser.py
author: ALESSANDRO QUERENGHI
id:     IN2300001

This file contains the classes required to parse the scene from JSON
"""

class SceneFormatException(ValueError):
    pass

class SceneLoadError(Exception):
    pass

class SceneParser:
    """
    Represents a scene for a 2D retro image

    This class offers functionality to read a scene file. This represents a
    retro 2D image, encoding what tiles are to be used for background, where to
    put sprites and their orientation and what color to treat as transparent

    Parameters
    ----------
    transparent_index : numpy.uint8
        The index of the color in the palette to be treated as transaprent for
        sprites
    tile_map : numpy.ndarray of numpy.uint8
        Background tiles. Each represents the index of a tile in the tile list
    sprites : list[dict]
        List of 'dict'. Each dict contains the index of the sprite to use, its
        position in the image and the transformations to apply

    Methods
    -------
    from_json(filename: str)
        Loads a scene from JSON file
    """
    def __init__(self, transparent_index: int, tile_map: ArrayLike, sprites: list[dict]):
        """
        Parameters
        ----------
        transparent_index : numpy.uint8
            The index of the color in the palette to be treated as transparent
        tile_map : ArrayLike
            The scene. Each element represents a tile in the tile list. The
            scene has size specified by 'SCENE_SHAPE'
        sprites : list of dict
            List of dicts. Each contains info about what sprite and where it
            should be placed. Also contains references to transformations

        Raises
        ------
        SceneFormatException
            If either the transparent index is not in range 'MAX_PALETTE_IDX',
            if the scene has the wrong shape, if the transformations are not
            valid or if the sprite or tile 'id' is out of range
        """
        try:
            # check the transparent_index
            transparent_index = np.uint8(transparent_index)
            if not transparent_index < MAX_PALETTE_IDX:
                raise ValueError(f"Transparency must be in range [0,"
                                 f" {MAX_PALETTE_IDX - 1}]: {transparent_index}")
            # check the scene
            scene = np.asarray(tile_map, dtype=np.uint8)
            if SCENE_SHAPE != scene.shape:
                raise ValueError("Tile map: wrong format")
            if np.any(scene > MAX_TILES):
                raise ValueError(f"Tiles ids are in the range [0, {MAX_TILES}],"
                                 f" got {scene.max()}")

            # check the sprites list
            if not isinstance(sprites, list):
                raise TypeError("'sprites' must be a list")
            for sprite in sprites:
                if not (0 <= sprite['id'] < MAX_SPRITES):
                    raise ValueError(f"There are only {MAX_SPRITES} available"
                                     f" sprites (got {sprite['id']})")
                if not isinstance(sprite['flip_h'], bool):
                    raise TypeError("'flip_h' must be either True or False")
                if not isinstance(sprite['flip_v'], bool):
                    raise TypeError("'flip_v' must be either True or False")
                if sprite['rotation'] not in ROTATIONS:
                    raise ValueError(f"rotation values must be one of"
                                     f" {ROTATIONS} (got {sprite['rotation']})")

            self.transparent_index = transparent_index
            self.tile_map = scene
            self.sprites = sprites
        except Exception as e:
            raise SceneFormatException(f"SceneParser initialization failed due"
                                       f" to: {e}")

    @classmethod
    def from_json(cls, filename: str) -> Self:
        """
        Parses a scene stored in a JSON file.

        Parameters
        ----------
        filename : str
            The JSON file that contains the scene data

        Raises
        ------
        SceneLoadError
            If either the file was not found, it is not JSON formatted or it
            doesn't contain the right fields
        """
        try:
            with open(filename, 'r') as f:
                o = json.load(f)
            return cls(o['transparent_index'], o['tile_map'], o['sprites'])
        except FileNotFoundError:
            raise SceneLoadError(f"The scene file '{filename}' could not be"
                                   f" found.")
        except json.JSONDecodeError as e:
            raise SceneLoadError(f"The scene file '{filename}' contains"
                                   f" invalid JSON: {e}")
        except ValueError as e:
            raise SceneLoadError(f"The scene file '{filename}' has invalid"
                                   f" data: {e}")
        
