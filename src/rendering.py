import numpy as np
from PIL import Image

class RenderingError(Exception):
    pass

class RenderingPipeline:
    def __init__(self, palette):
        self.palette = palette

    def render(self, frame_buffer, filename):
        try:
            frame_buffer = np.asarray(frame_buffer, dtype=np.uint8)
            rgb_buffer = self.palette[frame_buffer]
            img = Image.fromarray(rgb_buffer)
            img.save(filename)
            return None
        except ValueError:
            raise RenderingError("Wrong format for frame buffer")
        except OSError as e:
            raise RenderingError(f"Failed to save image file due to: {e}")
