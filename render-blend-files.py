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

def load_blend_objects_and_join(filepath, link=False):
    with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
        data_to.objects = data_from.objects

    added_mesh_objects = []
    for obj in data_to.objects:
        if obj is not None and obj.type == 'MESH':
            bpy.context.collection.objects.link(obj)
            added_mesh_objects.append(obj)

    if added_mesh_objects:
        # Make sure the first object is active and all others are selected
        bpy.context.view_layer.objects.active = added_mesh_objects[0]
        for obj in added_mesh_objects:
            obj.select_set(True)

        # Join objects
        bpy.ops.object.join()

    return bpy.context.active_object

# Function to process and render each model
def process_model(model_file_path, output_dir):
    model_name = os.path.splitext(os.path.basename(model_file_path))[0]
    shader_name = "Dotted lines shader"
    camera = bpy.data.objects['Camera']

    # Import and join objects from the .blend file
    imported_object = load_blend_objects_and_join(model_file_path)

    # Check if an object was imported and joined successfully
    if not imported_object:
        print(f"No object was imported from '{model_file_path}'. Skipping.")
        return

    print(f"Imported object: {imported_object.name}")

    # Select the imported object
    imported_object.select_set(True)

    # Generate UV map
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT')

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
    
    print(f"Output path: {output_path}")

    # Render the image
    bpy.ops.render.render(write_still=True)

def main():
    # Set the output directory
    output_directory = bpy.path.abspath("//output")

    # Use the current blend file's directory as the directory containing model files
    models_directory = bpy.path.abspath("//blend_files")
    if not models_directory:
        print("No directory selected. Exiting.")
        return

    # Process each model in the directory
    for file in os.listdir(models_directory):
        if file.endswith(".blend"):
            model_path = os.path.join(models_directory, file)
            print(f"Processing {model_path}")
            process_model(model_path, output_directory)
            print(f"Finished processing {model_path}")

    print("Script completed")

# Run the script
main()