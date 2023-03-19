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

# Function to scale an object to fit inside camera bounds
def scale_to_fit_camera_bounds(obj, camera):
    obj_dimensions = obj.dimensions
    camera_angle_x = bpy.data.cameras[camera.data.name].angle_x
    camera_angle_y = bpy.data.cameras[camera.data.name].angle_y
    
    aspect_ratio = bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y
    if aspect_ratio >= 1:
        camera_angle = camera_angle_x
    else:
        camera_angle = camera_angle_y

    obj_scale_x = (2 * math.tan(camera_angle_x / 2)) / obj_dimensions.x
    obj_scale_y = (2 * math.tan(camera_angle_y / 2)) / obj_dimensions.y
    required_scale = min(obj_scale_x, obj_scale_y) * 15

    obj.scale = (required_scale, required_scale, required_scale)

    # Apply the scale to the object
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)



# Function to process and render each model
def process_model(model_file_path, output_dir):
    model_name = os.path.splitext(os.path.basename(model_file_path))[0]

    bpy.ops.import_mesh.stl(filepath=model_file_path)

    imported_object = bpy.data.objects[model_name]
    imported_object.select_set(True)

    # Generate UV map
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT')

    # Center object
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    imported_object.location = (0, 0, 0)

    # Apply custom shader
    shader_name = "5. Dotted lines shader"
    apply_shader(imported_object, shader_name)

    # Scale object to fit camera bounds and rotate it
    camera = bpy.data.objects['Camera']
    center_camera_on_object(imported_object, camera)
    scale_to_fit_camera_bounds(imported_object, camera)
    imported_object.rotation_euler.z += math.radians(135)
    
    # Center object
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    imported_object.location = (0, 0, 0)
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.transform.resize(value=(0.95, 0.95, 0.95))
    
    ## FRONT RENDER

    # Set render output settings
    output_path = os.path.join(output_dir, f"{model_name}-front.png")
    bpy.context.scene.render.filepath = output_path

    # Render and save the image
    bpy.ops.render.render(write_still=True)\
    
    ## SIDE RENDER
    
    # Rotate 90 degrees further to get other side
    imported_object.rotation_euler.z += math.radians(90)
    
    output_path = os.path.join(output_dir, f"{model_name}-side.png")
    bpy.context.scene.render.filepath = output_path

    # Render and save the image
    bpy.ops.render.render(write_still=True)
    
    ## BACK RENDER
    
    # Rotate 90 degrees further to get other side
    imported_object.rotation_euler.z += math.radians(90)
    
    output_path = os.path.join(output_dir, f"{model_name}-side.png")
    bpy.context.scene.render.filepath = output_path

    # Render and save the image
    bpy.ops.render.render(write_still=True)
    
    ## TOP RENDER
    
    # Rotate for models that are placed on their backs
    imported_object.rotation_euler = (math.radians(120), 0, math.radians(215))
    bpy.ops.view3d.camera_to_view_selected()
    
    # Set render output settings
    output_path = os.path.join(output_dir, f"{model_name}-top.png")
    bpy.context.scene.render.filepath = output_path

    # Render and save the image
    bpy.ops.render.render(write_still=True)

    # Remove imported object from the scene
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    imported_object.select_set(True)
    bpy.ops.object.delete()

def main():
    # Set the output directory
    output_directory = bpy.path.abspath("//output")

    # Use the current blend file's directory as the directory containing model files
    models_directory = bpy.path.abspath("//stls")
    if not models_directory:
        print("No directory selected. Exiting.")
        return

    # Process each model in the directory
    for file in os.listdir(models_directory):
        if file.endswith(".stl"):
            model_path = os.path.join(models_directory, file)
            process_model(model_path, output_directory)

# Run the script
main()

# End