from src.config import *
from PIL import Image
import numpy as np
import json
from numpy.typing import ArrayLike, NDArray

"""
file:   palette.py 
author: ALESSANDRO QUERENGHI
id:     IN2300001

This files contains the classes that parse the palette
"""

class PaletteLoadError(Exception):
    pass

class Palette:
    """
    Class used to parse and represent a palette.

    A Palette represents a list of RGB values as a Numpy array of size
    MAX_PALETTE_IDX. RGB values are represented with arrays of three elements
    of type uint8.

    Attributes
    ----------
    palette : numpy.ndarray
        the stored palette

    Methods
    -------
    from_json(filename: str)
        reads a json file containing a palette and returns a Palette object
    from_png(*arg)
        Reads png images and obtains the palette from each
    """

    def __init__(self, palette: ArrayLike):
        """
        Parameters
        ----------
        palette : array_like
            the palette
        """
        self.palette = np.asarray(palette, dtype=np.uint8)
        if 3 != palette.shape[1]:
            raise ValueError(f"The palette is a triple of RGB values in the"
                             f" range [0, 255]")

    @classmethod
    def from_json(cls, filename: str) -> Self:
        """
        Instantiates a Palette from a JSON file

        Parameters
        ----------
        filename : str
            The JSON file to parse

        Raises
        ------
        PaletteLoadError
            If either the file is not found, it has wrong JSON formatting or
            contains invalid data
        """
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

    @classmethod
    def from_png(cls, *arg) -> Self:
        """
        Instantiates a palette from a list of files

        Beware that if not enough colors are taken from the images the creation
        of the Palette will fail

        Parameters
        ----------
        arg : str or list of strings
            The files from which to extract the palette
        """
        conca = np.empty((0, 3))
        for filename in arg:
            im = Image.open(filename)
            pal = im.quantize(16).getpalette()
            data = np.array(pal, dtype=np.uint8).reshape(-1, 3)
            conca = np.concat((conca, data), axis=0)
        data = np.unique(conca, axis=0)
        return cls(data)

    def __getitem__(self, i: int) -> NDArray[np.uint8]:
        """
        returns a single RGB value
        """
        return self.palette[i]

    def __repr__(self) -> str:
        """
        Returns the palette as the string representation of numpy.NDArray
        """
        return str(self.palette)


def main():
    p = Palette.from_png("sprites-dup.png", "tiles-dup.png")
    print(p)
    return None

if __name__ == "__main__":
    main()

