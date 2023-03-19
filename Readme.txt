To generate artwork:

Place STL files in the "stls" folder.

Open Blender file

Go to Scripts tab and text > open "render-script.py" if not already loaded.

Run the script.

Images will be generated (SLOWLY!) into the output directory.

---

NOTES:

It may take a long time before you see your first result, primarily due to the uv.smart_project() function, but this is necessary for the shader to render properly.
It will run faster on models that have better topology and fewer polys.

The script is stored as a separate .py file and linked into the Blender file.

---

The BLEND1 (backup) file will not be tracked by GitHub, so make sure your changes are saved in the correct file.

Make sure you leave the scene empty when done working on it. Existing files can disrupt the script. (automatically cleaning it on start might be a good improvement!)