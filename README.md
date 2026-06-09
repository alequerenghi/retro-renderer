# Retro 2D Rendering Engine (Python Component)

This project focuses on implementing a high-performance **2D retro-style graphics renderer** in Python using optimized array operations.

The engine processes an indexed color environment to composite a background tile map and dynamically transformed sprite structures into a final frame buffer.

---

## Architecture & Core Features

* 
**Indexed 16-Color Palette:** All asset graphics utilize 4 bits per pixel to index a single master color palette composed of 16 distinct RGB triplets (values ranging from 0 to 255).


* 
**640x480 Frame Buffer:** Displays a background grid split into 20 columns and 15 rows.


* 
**Layered Rendering Pipeline:** Composites the background tile map first, then overlays individual sprites in the exact order specified by the scene file.


* 
**Sprite Transformations:** Supports horizontal flipping, vertical flipping, and clockwise cardinal rotations (0°, 90°, 180°, 270°). Transformations are calculated prior to writing to the frame buffer.


* 
**Transparency Masking:** A dedicated transparency color index ensures that specific sprite pixels are ignored during composition, leaving the background asset visible beneath.


* 
**Boundary Clipping:** Gracefully handles sprites positioned partially or fully off-screen, rendering only the pixels that reside inside valid frame buffer space.



---

## Input File Formats & Assets

### 1. Palette File (`.json`)

A pure JSON array containing exactly 16 sub-arrays, each representing an `[R, G, B]` color configuration.

### 2. Sheet Assets (`.bin`)

Both the **Tile Sheet** (64 tiles of 32x32 pixels in an 8x8 grid) and the **Sprite Sheet** (16 sprites of 64x64 pixels in a 4x4 grid) are saved as 256x256 pixel matrices in a packed binary format.

* 
**Data Packing:** Each asset file is exactly **32,768 bytes** long.


* Every byte houses two distinct 4-bit pixels: the **high 4 bits (high nibble)** match the first pixel, and the **low 4 bits (low nibble)** match the subsequent pixel.



### 3. Scene Configuration File (`.json`)

A structured JSON file tracking three fields:

* 
`transparent_index`: The color index designated for sprite transparency.


* 
`tile_map`: A 15x20 matrix mapping the background tile layouts.


* 
`sprites`: A collection of objects tracking individual sprite parameters (`id`, `x`, `y`, `flip_h`, `flip_v`, `rotation`).



---

## Package Architecture

The renderer consists of 5 modular classes:

1. 
**`Palette`:** Parses the color JSON map, handles structural verification, and maps palette integers to raw RGB spaces.


2. 
**`VirtualVRAM`:** Imports the binary sheets and unpacks the 4-bit chunk patterns into 2D index arrays.


3. 
**`SceneParser`:** Reads the scene JSON to validate layout structures, handling data extraction for the blitting system.


4. 
**`Blitter`:** Extracts raw elements from VRAM, performs geometric translations (flips and rotations), filters transparency masks, and writes the bounding data blocks to the frame buffer.


5. 
**`RenderingPipeline`:** Coordinates the complete composition step, updates the frame buffer map to 24-bit RGB values, and interfaces with the Pillow library to output the final graphic.



---

## Command Line Interface (CLI)

The tool runs strictly via the command line interface with positional arguments. It bypasses interactive user input and outputs a single flattened PNG image.

```bash
python main.py <palette.json> <scene.json> <tiles.bin> <sprites.bin> <output.png>

```

### Argument Order:

1. 
`palette.json`: Path to the color map configuration.


2. 
`scene.json`: Path to the targeted scene arrangement.


3. 
`tiles.bin`: Path to the binary packed tile graphics sheet.


4. 
`sprites.bin`: Path to the binary packed sprite graphics sheet.


5. 
`output.png`: Path where the final rendered image will be saved.
