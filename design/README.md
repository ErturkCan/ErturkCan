# Profile design

Shared visual language with [Stip](https://getstip.com) and [erturks.com](https://erturks.com): olive, warm white, soft corners, thin lines and restrained typography. `tokens.json` records the palette, spacing and component values. GitHub controls the outer layout and text font.

Rebuild the SVG assets with `python scripts/build_assets.py`. Convert the two `assets/ce-vision-*.svg` files to PNG for GitHub using Sharp or another SVG renderer; these embed the demo image. All other cards use SVG directly.

Geometry data comes from [the polygon project's demo.py](https://github.com/ErturkCan/Regular_Polygons_Intersection/blob/main/demo.py), using the same functions as its numerical checks. The dots are computed intersections.

The computer-vision thumbnail is actual inference from **pretrained YOLOv8n COCO weights**, rendered through `utils.visualize.draw_detections`. It uses the [Ultralytics bus sample](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/assets/bus.jpg). It is not a defect-detection result, company footage or a production benchmark. Reproduce it with [assembly-line-cv/demo.py](https://github.com/ErturkCan/assembly-line-cv/blob/main/demo.py). Exact model outputs are in `assets/vision-result.json`.

Age and career status reflect September 2026 and are maintained manually. The short bio and personal wording remain in README.md.
