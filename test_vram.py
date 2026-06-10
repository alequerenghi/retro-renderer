from src import Palette, VirtualVRAM, Sprites,  Tiles
import json

def main():
    p = Palette.from_png("sprites.png", "tiles.png")
    with open("example/palette.json", "w") as f:
        json.dump(p.palette.tolist(), f)
    s = Sprites.from_png("sprites.png", p)
    t = Tiles.from_png("tiles.png", p)
    s.to_bin("example/sprites.bin")
    t.to_bin("example/tiles.bin")
    return None

if __name__ == "__main__":
    main()

