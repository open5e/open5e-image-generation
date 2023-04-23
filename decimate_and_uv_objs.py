import bpy
import os
import winsound

# Function to play a system sound
def play_system_sound():
    winsound.MessageBeep()

# Define the directory paths
source_directory = bpy.path.abspath("//obj_files")
output_directory = bpy.path.abspath("//obj_optimized")
sound_file_path = "/path/to/your/sound_file.wav"  # Replace with the path to your sound file

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Set the target number of vertices
target_points = 250000

# Iterate through the files in the source directory
for file_name in os.listdir(source_directory):
    # Check if the file has the .obj extension
    if file_name.endswith(".obj"):
        # Create the file paths
        obj_file_path = os.path.join(source_directory, file_name)
        processed_obj_file_path = os.path.join(output_directory, file_name)
        
        # Import the .obj file
        bpy.ops.import_scene.obj(filepath=obj_file_path)
        
        # Get the imported object
        imported_obj = bpy.context.selected_objects[0]
        
        # Join all the mesh objects
        bpy.ops.object.select_all(action='SELECT')
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        if len(selected_objects) > 1:
            bpy.context.view_layer.objects.active = selected_objects[0]
            bpy.ops.object.join()
            imported_obj = bpy.context.active_object
        else:
            bpy.context.view_layer.objects.active = selected_objects[0]
            imported_obj = bpy.context.active_object

        # Check if the mesh has more than the target number of triangles
        if len(imported_obj.data.vertices) > target_points:
            decimation_ratio = min(1.0, target_points / len(imported_obj.data.vertices))

            # Add and configure the Decimate modifier
            decimate_modifier = imported_obj.modifiers.new("Decimate", "DECIMATE")
            decimate_modifier.decimate_type = "COLLAPSE"
            decimate_modifier.use_collapse_triangulate = True
            decimate_modifier.ratio = decimation_ratio

            # Apply the Decimate modifier
            bpy.ops.object.modifier_apply({"object": imported_obj}, modifier=decimate_modifier.name)
        
        # Add and configure Smart UV Project
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.smart_project()
        bpy.ops.object.mode_set(mode="OBJECT")

        # Export the processed .obj file
        bpy.ops.export_scene.obj(filepath=processed_obj_file_path, use_selection=True, use_materials=False)

        # Delete the imported object
        bpy.ops.object.select_all(action="DESELECT")
        imported_obj.select_set(True)
        bpy.ops.object.delete()

print("Finished processing all .obj files.")
play_system_sound()  # Play the sound after the script finishes