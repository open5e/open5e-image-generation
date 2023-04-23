import bpy
import os
import math

# Function to apply a shader to a given object
def apply_shader(obj, shader_name):
    material = bpy.data.materials.get(shader_name)
    if not material:
        raise Exception(f"Material '{shader_name}' not found.")

    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

def center_camera_on_object(obj, camera, distance=12):
    obj_location = obj.location
    camera.rotation_euler.x = math.radians(-90)
    camera.rotation_euler.y = math.radians(180)
    camera.rotation_euler.z = 0
    camera.location = (obj_location.x, obj_location.y + distance, obj_location.z)

def import_obj(filepath):
    bpy.ops.import_scene.obj(filepath=filepath)
    imported_obj = bpy.context.selected_objects[0]
    return imported_obj

# Function to process and render each model
def process_model(model_file_path, output_dir):
    model_name = os.path.splitext(os.path.basename(model_file_path))[0]
    shader_name = "Dotted lines shader.rimlight"
    camera = bpy.data.objects['Camera']

    # Import the .obj file
    imported_object = import_obj(model_file_path)

    print(f"Imported object: {imported_object.name}")

    # Apply custom shader
    apply_shader(imported_object, shader_name)

    # Position camera
    center_camera_on_object(imported_object, camera)

    # Center object
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    imported_object.location = (0, 0, 0)
    bpy.ops.view3d.camera_to_view_selected()
    
    ## FRONT RENDER

    # Set render output settings
    output_path = os.path.join(output_dir, f"{model_name}-front.png")
    bpy.context.scene.render.filepath = output_path

    # Render the image
    bpy.ops.render.render(write_still=True)

def main():
    # Set the output directory
    output_directory = bpy.path.abspath("//output")

    # Use the current blend file's directory as the directory containing model files
    models_directory = bpy.path.abspath("//obj_files")
    if not models_directory:
        print("No directory selected. Exiting.")
        return

    # Process one .obj file for testing purposes
    test_file = "Aarakocra.obj"  # Replace this with the name of one of your .obj files
    model_path = os.path.join(models_directory, test_file)
    print(f"Processing {model_path}")
    process_model(model_path, output_directory)
    print(f"Finished processing {model_path}")

    print("Script completed")

# Run the script
main()