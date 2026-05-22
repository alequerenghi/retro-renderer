from src.config import MAX_PALETTE_IDX, SCENE_SHAPE, MAX_SPRITES, ROTATIONS
import numpy as np
import json

class SceneFormatException(ValueError):
    pass

class SceneLoadError(Exception):
    pass

class SceneParser:
    def __init__(self, transparent_index, tile_map, sprites):
        try:
            if not (0 <= transparent_index < MAX_PALETTE_IDX):
                raise ValueError(f"Transparency must be in range [0,"
                                 f" {MAX_PALETTE_IDX - 1}]: {transparent_index}")

            scene = np.asarray(tile_map, dtype=np.uint8)
            if SCENE_SHAPE != scene.shape:
                raise ValueError("Tile map: wrong format")

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
        except Exception as e:
            raise SceneFormatException(f"SceneParser initialization failed due"
                                       f" to: {e}")

        self.transparent_index = transparent_index
        self.tile_map = scene
        self.sprites = sprites

    @classmethod
    def from_json(cls, filename):
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
        
