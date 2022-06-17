# Levels

## Filesystem directory

```
levels/
├─ level_1/
│  ├─ bounds.bmp
│  ├─ texture.jpg
│  ├─ parameters.json
├─ race_track/
│  ├─ ...
README.md
```

## Level files

- `bounds.bmp` is a 2bit bitmap (to do that use ImageMagick: `convert image.png -colors 4 bounds.bmp) containing:
  - The playable area in white
  - The out-of-bounds area in black
  - A light grey (#ababab) line which when touched awards the racer a point
  - A dark grey (#555555) line which when touched signals a win

- `texture.jpg` is a jpeg image containing the background texture

- `parameters.json` is a json file containing the following parameters:
  - `width`: the width of the level in pixels
  - `height`: the height of the level in pixels
  - `start`: the starting position of the racer in pixels and angle in degrees
  - `checkpoints`: the number of checkpoints required to win

## Notes

- Do not place checkpoints "behind" the starting racer position.
