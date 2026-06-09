from src.config import *
from src.palette import Palette
import numpy as np
from PIL import Image
from numpy.typing import ArrayLike, NDArray

"""
file:   virtualvram.py
author: ALESSANDRO QUERENGHI
id:     IN2300001

This file contains the classes that read and unpack binary data of sprites and
tiles
"""

class SheetDataLoadError(Exception):
    pass

class SheetData:
    """
    Represents a data asset

    Superclass of tiles and sprites which defines standard methods to create
    and access asset objects

    Attributes
    ----------
    size : int
        The size (also in bytes) of an asset. It refers to the length of one
        side
    data : numpy.ndarray of numpy.uint8
        Asset data

    Methods
    -------
    fromfile(filename : str)
        Loads and unpacks an asset file containing binary data 
    to_png(palette : Palette, filename : str)
        Writes data to the file indicated using the palette passed
    from_png(filename : str, palette : Palette)
        Loads an asset object from PNG image and quantizes the palette to the
        vlaue passed
    to_bin(filename : str)
        Packs the numpy.uint8' array representing an asset object into a 4bit
        arraay of nibblles and saves it to the filename passed
    """

    def __init__(self, data: ArrayLike, size: int):
        self.size = size
        self.data = np.asarray(data, dtype=np.uint8)

    @classmethod
    def fromfile(cls, filename: str) -> Self:
        """
        Loads and unpacks an asset file containing binary data.

        Asset files store asset data in 4 bits, data is read and unpacked into
        numpy.uint8 arrays

        Parameters
        ----------
        filename : str
            The path to the asset to load

        Raises
        ------
        SheetDataLoadError
            If 'filename' isn't found, if the file contains invalid data
        """
        try:
            with open(filename, "rb") as f:
                # loads binary data into memory
                packed = np.fromfile(f, dtype=np.uint8)
            # check data size
            if (SHEET_SIZE ** 2 // 2 != packed.shape[0]):
                raise ValueError(f"Asset file '{filename}' is corrupted or"
                                 f" wrong size. Expected {SHEET_SIZE // 2} bytes,"
                                 f" but got {packed.shape[0]} bytes")
            # unpack data: even indices get most significant bits while odd
            # ones get the least significant bits
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

    @classmethod
    def from_png(cls, filename: str, palette: Palette) -> Self:
        """
        Loads an asset from a PNG file and applies the given palette
        to it
        """
        img = Image.open(filename).convert("RGB")
        flat_palette = palette.palette.flatten().tolist()
        # create new image from the palette
        template = Image.new("P", (1,1))
        template.putpalette(flat_palette)
        # now quantize the png to the obtained
        quantized = img.quantize(palette=template,
                                 dither=Image.Dither.NONE)
        return cls(quantized, cls.size)

    def __getitem__(self, k: int) -> NDArray[np.uint8]:
        """
        Returns a view of an asset object
        """
        items_per_row   = SHEET_SIZE // self.size
        start_row       = self.size * (k // items_per_row)
        start_col       = self.size * (k % items_per_row)
        return self.data[start_row : start_row + self.size,
                         start_col : start_col + self.size]

    def to_png(self, palette: Palette, filename: str):
        """
        Save an asset to 'filename' using the palette 'palette'
        """
        rgb_buffer = palette[self.data]
        img = Image.fromarray(rgb_buffer)
        img.save(filename)
        return None

    def to_bin(self, filename: str):
        """
        Packs data into nibbles and saves to file
        """
        data    = self.data.flatten()
        outdata = np.empty(data.shape[0] // 2, dtype=np.uint8)
        outdata = data[0::2] << 4 & 0xf0 | data[1::2] & 0x0f
        outdata.tofile(filename)
        return None

class Sprites(SheetData):
    """
    Subclass of 'SheetData' which redefines the size of a sprite
    """
    size = SPRITE_SIZE

class Tiles(SheetData):
    """
    Subclass of 'SheetData' which redefines the size of a tile
    """
    size = TILE_SIZE

class VirtualVRAM:
    """
    Loads into memory sprites and tiles

    Attributes
    ----------
    tiles : Tiles
        The tiles loaded
    sprites : Sprites
        The sprites loaded

    Methods
    -------
    fromfiles(tiles: str, sprites: str)
        Loads tiles and sprites from the respective files
    to_png(palette: Palette, tiles: str, sprites: str)
        Saves tiles and sprites using the palette to the files indicated
    """
    def __init__(self, tiles: Tiles, sprites: Sprites):
        """
        Parameters
        ----------
        tiles : Tiles
            The tiles loaded
        sprites : Sprites
            The sprites loaded
        """
        self.tiles      = tiles
        self.sprites    = sprites

    @classmethod
    def fromfiles(cls, tiles: str, sprites: str) -> Self:
        """
        Loads tiles and sprites from files

        Parameters
        ----------
        tiles : str
            The file name where the tiles asset is found
        sprites : str
            The file name where the sprites asset is found
        """
        return cls(
                tiles=Tiles.fromfile(tiles),
                sprites=Sprites.fromfile(sprites)
        )

    def to_png(self, palette, tiles: str, sprites: str):
        """
        Save tiles and sprites to png file

        Parameters
        ----------
        palette : Palette
            The palette to use
        tiles : str
            File name where to save tiles object
        sprites : str
            File name where to save sprites object
        """
        self.tiles.to_png(palette, tiles)
        self.sprites.to_png(palette, sprites)
