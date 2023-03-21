import os
import bpy

def remove_creature_objects(filepath):
    bpy.ops.wm.open_mainfile(filepath=filepath)

    for obj in bpy.data.objects:
        if "Creature" in obj.name:
            bpy.data.objects.remove(obj, do_unlink=True)

    bpy.ops.wm.save_mainfile(filepath=filepath)

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".blend"):
                filepath = os.path.join(root, file)
                remove_creature_objects(filepath)

if __name__ == "__main__":
    directory_path = r"C:\Users\Ean\monster_manual_files"
    process_directory(directory_path)