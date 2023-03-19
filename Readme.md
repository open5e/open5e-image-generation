### To generate artwork:

1. Place STL files in the "stls" folder.
2. Open Blender file
3. Go to Scripts tab and text > open "render-script.py" if not already loaded.
4. Run the script.
5. Images will be generated (SLOWLY!) into the output directory.

The script will generate 4 images each: front, side, back and top. This is because the initial source oriented models optimized for 3d-printing, not render, so there's no predicting the orientation. I've found this is sufficient to get a good shot of most models. Some may require some tweaking or custom renders, I leave that as an exercise to the reader. :)

### NOTES

It may take a long time before you see your first result, primarily due to the uv.smart_project() function, but this is necessary for the shader to render properly.
It will run faster on models that have better topology and fewer polys.

The script is stored as a separate .py file and linked into the Blender file.


### Developer Notes

The BLEND1 (backup) file will not be tracked by GitHub, so make sure your changes are saved in the correct file.

Make sure you leave the scene empty when done working on it. Existing files can disrupt the script. (automatically cleaning it on start might be a good improvement!)