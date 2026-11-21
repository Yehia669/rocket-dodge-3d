import bpy
import math
import os
from mathutils import Vector

OUT = r"C:\Users\abdel\OneDrive\Documents\Default Project\rocket_game_v2\rocket.glb"
BLEND = r"C:\Users\abdel\OneDrive\Documents\Default Project\rocket_game_v2\rocket_clean.blend"


def clean():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for c in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for b in list(c):
            if b.users == 0:
                c.remove(b)


def material(name, color, rough=.45, metal=0.0, emit=None, strength=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1)
        p.inputs['Emission Strength'].default_value = strength
    return m


def put(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj


def fin(name, angle, mat):
    u = Vector((math.cos(angle), math.sin(angle), 0))
    v = Vector((-math.sin(angle), math.cos(angle), 0))
    z0, z1 = .25, 1.35
    p1 = u*.34 + Vector((0,0,z0)); p2 = u*.78 + Vector((0,0,z0)); p3 = u*.34 + Vector((0,0,z1))
    t = .055
    verts = [p1-v*t, p2-v*t, p3-v*t, p1+v*t, p2+v*t, p3+v*t]
    faces = [(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)]
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(x) for x in verts], [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return put(o, mat)


clean()
red = material('Rocket Red', (.82,.04,.05), .35, .35)
white = material('Nose White', (.96,.96,.92), .4)
blue = material('Fin Blue', (.04,.28,.85), .38, .3)
win = material('Window Blue', (.03,.35,.8), .15, .2, emit=(.05,.3,.7), strength=.8)
flame = material('Flame Orange', (1,.35,.02), .3, emit=(1,.3,0), strength=6)

bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=.5, depth=2.4, location=(0,0,1.4))
put(bpy.context.active_object, red).name = 'Rocket Body'

bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=.505, depth=.3, location=(0,0,1.2))
put(bpy.context.active_object, white).name = 'White Stripe'

bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=.5, radius2=0, depth=.9, location=(0,0,3.05))
put(bpy.context.active_object, red).name = 'Nose Cone'

bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=.16, radius2=0, depth=.3, location=(0,0,3.65))
put(bpy.context.active_object, white).name = 'White Tip'

for i in range(3):
    fin('Blue Fin %d' % (i+1), i*2*math.pi/3, blue)

bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=.2, location=(0,-.5,1.9))
w = bpy.context.active_object
w.scale = (1, .25, 1)
put(w, win).name = 'Window Blue'

bpy.ops.mesh.primitive_torus_add(major_radius=.21, minor_radius=.035, major_segments=12, minor_segments=6,
                                 location=(0,-.52,1.9), rotation=(math.pi/2,0,0))
put(bpy.context.active_object, white).name = 'Window Ring'

bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=.35, radius2=0, depth=.9,
                                location=(0,0,-.25), rotation=(math.pi,0,0))
put(bpy.context.active_object, flame).name = 'Flame Orange'

bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=.18, radius2=0, depth=.6,
                                location=(0,0,-.05), rotation=(math.pi,0,0))
put(bpy.context.active_object, white).name = 'Flame Core'

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=False, export_apply=True)
print('CLEAN_ROCKET_SAVED', OUT, os.path.getsize(OUT))
