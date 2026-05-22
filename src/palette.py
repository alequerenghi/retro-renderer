from src.config import MAX_PALETTE_IDX
import numpy as np
import json

class PaletteLoadError(Exception):
    pass

class Palette:
    def __init__(self, palette):
        self.palette = np.asarray(palette, dtype=np.uint8)
        if (MAX_PALETTE_IDX, 3) != palette.shape:
            raise ValueError(f"Palette shape must be ({MAX_PALETTE_IDX}, 3), "
                             f"current palette: {palette.shape}")

    @classmethod
    def from_json(cls, filename):
        try:
            with open(filename) as f:
                data = json.load(f)
            return cls(np.array(data, dtype=np.uint8))
        except FileNotFoundError:
            raise PaletteLoadError(f"The palette file '{filename}' could not be"
                                   f" found.")
        except json.JSONDecodeError as e:
            raise PaletteLoadError(f"The palette file '{filename}' contains"
                                   f" invalid JSON: {e}")
        except ValueError as e:
            raise PaletteLoadError(f"The palette file '{filename}' has invalid"
                                   f" data: {e}")

    def __getitem__(self, i):
        return self.palette[i]
