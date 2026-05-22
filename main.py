from src import *
import sys

def main():
    if 6 != len(sys.argv):
        raise ValueError("missing argument: execute retro-renderer with the"
                         f" command:\npython main.py <palette.json> <scene.json>"
                         f" <tiles.bin> <sprites.bin> <output.png>")
    p   = Palette.from_json(sys.argv[1])
    s   = SceneParser.from_json(sys.argv[2])
    v   = VirtualVRAM.fromfiles(sys.argv[3], sys.argv[4])
    b   = Blitter(v)
    r   = RenderingPipeline(p)
    fb  = b.gen_scene(s)
    r.render(fb, sys.argv[5])


if __name__ == "__main__":
    main()
