from src.config import *
from src.palette import Palette
import numpy as np
from PIL import Image

"""
file:   rendering.py 
author: ALESSANDRO QUERENGHI
id:     IN2300001

This file contains the classes required to generate the PNG image from the
scene
"""

class RenderingError(Exception):
    pass

class RenderingPipeline:
    """
    Class to convert a scene to PNG and write it to disk.

    Attributes
    ----------
    palette : Palette
        The palette used when rendering the scene

    Methods
    -------
    render(frame_buffer: numpy.NDArray[numpy.uint8], filename: str)
        Applies the palette to the frame buffer, converts it to 'PIL.Image' and
        writes it as PNG
    """
    def __init__(self, palette: Palette):
        """
        Parameters
        ----------
        palette : Palette
            The palette object to be used
        """
        self.palette = palette

    def render(self, frame_buffer: ArrayLike, filename: str):
        """
        Writes the scene to PNG

        Parameters
        ----------
        frame_buffer : ArrayLike
            The scene, an 2D array of pixels. Each pixel is the index of a RGB
            color in the palette
        filename : str
            The file to which the PNG is saved

        Raises
        ------
        RenderingError
            if the 'frame_buffer' cannot be converted to np.ndarray of
            numpy.uint8 or if the image can't be saved to file
        """
        try:
            if ".png" not in filename:
                raise ValueError(f"Please write image in PNG format. Add"
                                 f" '.png' after {filename}")
            # check that the frame buffer has the right format
            frame_buffer = np.asarray(frame_buffer, dtype=np.uint8)
            if np.any(frame_buffer > MAX_PALETTE_IDX):
                raise ValueError(f"The scene must contain values in the range"
                                 f" [0, {MAX_PALETTE_IDX}], got"
                                 f" {frame_buffer.max()}")
            # apply the palette to the scene. This converts the scene to 3D
            # array where dims 1 and 2 are the height and width of the image
            # and dim 3 is a triple of values in the range [0, 255], that is
            # RGB colors. Now the scene is a double array of RGB values
            rgb_buffer = self.palette[frame_buffer]
            # Convert to image and write to file
            img = Image.fromarray(rgb_buffer)
            img.save(filename)
            return None
        except ValueError as e:
            raise RenderingError(f"Wrong format for frame buffer: {e}")
        except OSError as e:
            raise RenderingError(f"Failed to save image file due to: {e}")
