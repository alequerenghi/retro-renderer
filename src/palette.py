from src.config import MAX_PALETTE_IDX
import numpy as np
import json

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
    """

    def __init__(self, palette):
        """
        Parameters
        ----------
        palette : array_like
            the palette
        """
        self.palette = np.asarray(palette, dtype=np.uint8)
        if (MAX_PALETTE_IDX, 3) != palette.shape:
            raise ValueError(f"Palette shape must be ({MAX_PALETTE_IDX}, 3), "
                             f"current palette: {palette.shape}")

    @classmethod
    def from_json(cls, filename):
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

    def __getitem__(self, i):
        """
        returns a single RGB value
        """
        return self.palette[i]
