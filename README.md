# TODO

## CLASSES

### VirtualRAM
- Load tile and sprite sheets
- decode 4 bit sequences into uint8 numpy arrays
- get each bit of each item, maybe a view? maybe reshaped into a tile or sprite?

Fields:
- Tiles
- Sprites

### SceneParser
- Load JSON of scene and return description of the background and sprites
- make sure that all elements are present
- save scene to JSON?

Fields:
- transparency_value
- Scene
- sprites

Things to do:
- check transparency value
- put scene into uint8 array (also checking size)
- check that each sprite has the right elements

### Blitter
- Extract tile and sprite from sheets, apply flip and rotations and transparency and copy results in frame buffer
- creates the frame buffer
- references all required info

Fields:
- VirtualVRAM
- frame buffer

Things to do:
- apply tile sheets to frame buffer
- apply (rotate and flip if necessary) sprites to buffer

### Palette
- Load and validate a 16 color palette;
- Return RGB values of colors

Fields:
- data

### RenderingPipeline
- convert frame buffer into RGB and save to PNG

Fields:
- Palette
- Frame buffer

Todo:
+ convert frame buffer to PNG
