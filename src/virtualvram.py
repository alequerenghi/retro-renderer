from src.config import SHEET_SIZE, SPRITE_SIZE, TILE_SIZE
from src.palette import Palette
import numpy as np
from PIL import Image

class SheetDataLoadError(Exception):
    pass

class SheetData:
    def __init__(self, data, size):
        self.size = size
        self.data = np.asarray(data, dtype=np.uint8)

    @classmethod
    def fromfile(cls, filename):
        try:
            with open(filename, "rb") as f:
                packed = np.fromfile(f, dtype=np.uint8)
            if (SHEET_SIZE ** 2 // 2 != packed.shape[0]):
                raise ValueError(f"Asset file '{filename}' is corrupted or"
                                 f" wrong size. Expected {SHEET_SIZE // 2} bytes,"
                                 f" but got {packed.shape[0]} bytes"
                                 )
            data        = np.empty(SHEET_SIZE ** 2, dtype=np.uint8)
            data[0::2]  = (packed >> 4 ) & 0x0f
            data[1::2]  = packed & 0x0f
            return cls(data.reshape(SHEET_SIZE, SHEET_SIZE), cls.size)
        except FileNotFoundError:
            raise SheetDataLoadError(f"The asset file '{filename}' could not be"
                                   f" found.")
        except ValueError as e:
            raise SheetDataLoadError(f"The asset file '{filename}' has invalid"
                                   f" data: {e}")

    def __getitem__(self, k):
        items_per_row   = SHEET_SIZE // self.size
        start_row       = self.size * (k // items_per_row)
        start_col       = self.size * (k % items_per_row)
        return self.data[start_row : start_row + self.size,
                         start_col : start_col + self.size
                ]

    def to_png(self, palette, filename):
        rgb_buffer = palette[self.data]
        img = Image.fromarray(rgb_buffer)
        img.save(filename)
        return None

class Sprites(SheetData):
    size = SPRITE_SIZE

class Tiles(SheetData):
    size = TILE_SIZE

class VirtualVRAM:
    def __init__(self, tiles, sprites):
        self.tiles      = tiles
        self.sprites    = sprites

    @classmethod
    def fromfiles(cls, tiles, sprites):
        return cls(
                tiles=Tiles.fromfile(tiles),
                sprites=Sprites.fromfile(sprites)
        )

    def to_png(self, palette, tiles, sprites):
        self.tiles.to_png(palette, tiles)
        self.sprites.to_png(palette, sprites)
        

def main():
    p = Palette.from_json('example/palette.json')
    v = VirtualVRAM.fromfiles('example/tiles.bin', 'example/sprites.bin')
    v.to_png(p, 'tiles-dup.png', 'sprites-dup.png')
    return None

if __name__ == "__main__":
    main()

