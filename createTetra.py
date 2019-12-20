import bpy
import bmesh
import mathutils as mu

scale = 0.1

materQuartz = False
for material in bpy.data.materials:
    if material.name == 'Quartz':
        materQuartz = material

# Create Quartz Material
if materQuartz == False:
    materQuartz = bpy.data.materials.new(name="Quartz")
    materQuartz.use_nodes = True
    materQuartz.diffuse_color = ( 0.283, 0.424, 1.000)
    # Create Shaders
    materQuartz.node_tree.nodes.remove(materQuartz.node_tree.nodes[1]) # Remove the unnecessary diffuse shader
    materQuartz.node_tree.nodes.new(type="ShaderNodeRGB")
    materQuartz.node_tree.nodes['RGB'].outputs[0].default_value = (0.283, 0.424, 1.000, 1.000)
    materQuartz.node_tree.nodes.new(type="ShaderNodeBsdfTransparent") # Transparent BSDF
    materQuartz.node_tree.nodes.new(type="ShaderNodeBsdfGlossy") # Transparent BSDF
    materQuartz.node_tree.nodes['Glossy BSDF'].inputs[1].default_value = 0.15
    materQuartz.node_tree.nodes.new(type="ShaderNodeMixShader") # "Mix Shader"
    materQuartz.node_tree.nodes['Mix Shader'].inputs[0].default_value = 0.2
    # Connect Shaders
    materQuartz.node_tree.links.new(materQuartz.node_tree.nodes['RGB'].outputs[0],
                                    materQuartz.node_tree.nodes['Transparent BSDF'].inputs[0])
    materQuartz.node_tree.links.new(materQuartz.node_tree.nodes['RGB'].outputs[0],
                                    materQuartz.node_tree.nodes['Glossy BSDF'].inputs[0])
    materQuartz.node_tree.links.new(materQuartz.node_tree.nodes['Transparent BSDF'].outputs[0],
                                    materQuartz.node_tree.nodes['Mix Shader'].inputs[1])
    materQuartz.node_tree.links.new(materQuartz.node_tree.nodes['Glossy BSDF'].outputs[0],
                                    materQuartz.node_tree.nodes['Mix Shader'].inputs[2])
    materQuartz.node_tree.links.new(materQuartz.node_tree.nodes['Mix Shader'].outputs[0],
                                    materQuartz.node_tree.nodes['Material Output'].inputs[0])

# A function to spawn individual tetrahedra
def spawnTetra(vertices):
    # Calculate center
    center = [0, 0, 0]
    for vertex in vertices:
        center = [ center[0] + vertex[0],
                   center[1] + vertex[1],
                   center[2] + vertex[2]]
    center = [x/4.0 for x in center]
    # Recenter Mesh
    vertices = [[x[0]-center[0],x[1]-center[1],x[2]-center[2]] for x in vertices]
    # Create a mesh
    myMesh = bpy.data.meshes.new("NewMesh")
    # Create an object
    myObject = bpy.data.objects.new("Tetra", myMesh)
    myObject.location = tuple(center)
    # Associate the object with this scene
    scene = bpy.context.scene
    scene.objects.link(myObject)
    # scene.objects.active = myObject
    # myObject.select = True
    # Create a BMesh
    bm = bmesh.new()
    # Add vertices to the BMesh
    for v in vertices:
        bm.verts.new(v)
    # Add faces to the BMesh
    bm.verts.ensure_lookup_table()
    for i in range(4):
        J = 0 + (i == 0)
        K = 1 + (i < 2)
        L = 3 - (i == 3)
        temp1 = bm.verts[J].co
        temp2 = bm.verts[K].co
        temp3 = bm.verts[L].co
        faceC = (temp1 + temp2 + temp3) / 3
        cross = (temp2 - temp1).cross(temp3 - temp1)
        direction = cross.dot(faceC)
        if direction > 0:
            bm.faces.new([bm.verts[J], bm.verts[K], bm.verts[L]])
        else:
            bm.faces.new([bm.verts[J], bm.verts[L], bm.verts[K]])
    bm.normal_update()
    bm.to_mesh(myMesh)
    # Free the BMesh
    bm.free()
    # Assign a material
    myObject.data.materials.append(materQuartz)

# Open a file, loop through all the parameters and spawn tetrahedra
inFile = open("tetraList.txt", "r")
for tetra in inFile:
# for num in range(10):
    # tetra = inFile.readline()
    vertString = tetra.split(" ")
    vertices = [scale*float(x) for x in vertString]
    spawnTetra([vertices[0:3], vertices[3:6], vertices[6:9], vertices[9:]])

