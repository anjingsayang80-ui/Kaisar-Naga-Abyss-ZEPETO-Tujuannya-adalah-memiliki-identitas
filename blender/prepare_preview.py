"""
Kaisar Naga Abyss — Blender preview helper
Run from Blender's Scripting workspace. This creates a presentation preview only.
It does NOT fit the garment to ZEPETO, create UVs, rig, or transfer weights.
Keep the OBJ and MTL together at the paths configured below.
"""
import bpy
import math
from mathutils import Vector
from pathlib import Path

# Edit this path to the downloaded repository location on your computer.
OBJ_PATH = Path(r"./assets/kaisar_naga_abyss.obj")
OUTPUT_PATH = Path(r"./kaisar_naga_abyss_preview.png")

if not OBJ_PATH.exists():
    raise FileNotFoundError(
        f"OBJ not found: {OBJ_PATH.resolve()} — set OBJ_PATH to the downloaded file."
    )

# Start with a clean scene.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# Import the OBJ. Blender 4.x and earlier use different operators.
if hasattr(bpy.ops.wm, "obj_import"):
    bpy.ops.wm.obj_import(filepath=str(OBJ_PATH.resolve()))
else:
    bpy.ops.import_scene.obj(filepath=str(OBJ_PATH.resolve()), use_split_objects=True)

mesh_objects = [o for o in bpy.context.scene.objects if o.type == "MESH"]
if not mesh_objects:
    raise RuntimeError("The OBJ imported, but no mesh objects were found.")

# Improve viewport readability without changing the underlying silhouette.
for obj in mesh_objects:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    obj.select_set(False)

# Compute bounds and frame a three-quarter view.
corners = []
for obj in mesh_objects:
    corners.extend([obj.matrix_world @ Vector(c) for c in obj.bound_box])
minimum = Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners)))
maximum = Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners)))
center = (minimum + maximum) * 0.5
span = max((maximum - minimum).length, 1.0)

def aim(obj, point):
    direction = Vector(point) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

camera_data = bpy.data.cameras.new("AbyssPreviewCamera")
camera = bpy.data.objects.new("AbyssPreviewCamera", camera_data)
bpy.context.collection.objects.link(camera)
camera.location = center + Vector((span * 1.25, -span * 2.4, span * 0.65))
aim(camera, center)
camera.data.type = "ORTHO"
camera.data.ortho_scale = span * 1.45
bpy.context.scene.camera = camera

# Soft studio lighting.
def area_light(name, offset, energy, size):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = center + Vector(offset) * span
    aim(obj, center)
    return obj

area_light("Key_Softbox", (1.5, -1.5, 1.8), 1500, span * 1.2)
area_light("Fill_Softbox", (-1.8, -0.8, 0.6), 900, span * 1.4)
area_light("Rim_Softbox", (0.2, 1.6, 1.4), 1800, span * 0.9)

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT" if hasattr(bpy.types, "BLENDER_EEVEE_NEXT") else "BLENDER_EEVEE"
scene.render.resolution_x = 1200
scene.render.resolution_y = 1200
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(OUTPUT_PATH.resolve())
scene.world.color = (0.035, 0.035, 0.045)
scene.view_settings.view_transform = "Standard"

bpy.ops.render.render(write_still=True)
print(f"Preview saved to: {OUTPUT_PATH.resolve()}")
print("Reminder: preview only; avatar fitting, UVs, rigging and validation remain unfinished.")
