import bpy
import bmesh
import math

# Carbon, Hydrogen, Nitrogen
atomicRadii = [0.1, 0.1, 0.1]
atomicColors = [ (0.30984,    0.30984,    0.97263,    1.00000),
                 (0.53666,    0.53666,    0.91542,    1.00000),
                 (0.72443,    0.72443,    0.83952,    1.00000),
                 (0.75260,    0.75260,    0.82547,    1.00000),
                 (0.80000,    0.80000,    0.80000,    1.00000),
                 (0.81339,    0.77563,    0.77563,    1.00000),
                 (0.82547,    0.75260,    0.75260,    1.00000),
                 (0.82873,    0.74619,    0.74619,    1.00000),
                 (0.84380,    0.71554,    0.71554,    1.00000),
                 (0.84806,    0.70654,    0.70654,    1.00000),
                 (0.87727,    0.64000,    0.64000,    1.00000) ]
bondRadius = 0.1
hydBondSpacing = 0.2
hydBondRadius = 0.05
hydBondSegs = 6
atomList = []

# Create or find and return the requested material
def makeMaterial(atomName, color):
    for material in bpy.data.materials:
        if material.name == atomName:
            return material
    # Create Material
    returnMater = bpy.data.materials.new(name=atomName)
    returnMater.use_nodes = True
    returnMater.diffuse_color = color[:3]
    # Create Shaders
    returnMater.node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = color
    returnMater.node_tree.nodes['Diffuse BSDF'].inputs[1].default_value = 1.0
    returnMater.node_tree.nodes.new(type="ShaderNodeBsdfGlossy") # "Glossy BSDF"
    returnMater.node_tree.nodes['Glossy BSDF'].inputs[0].default_value = color
    returnMater.node_tree.nodes['Glossy BSDF'].inputs[1].default_value = 0.15
    returnMater.node_tree.nodes.new(type="ShaderNodeMixShader") # "Mix Shader"
    returnMater.node_tree.nodes['Mix Shader'].inputs[0].default_value = 0.1
    # Link Shaders
    returnMater.node_tree.links.remove(returnMater.node_tree.links[0])
    returnMater.node_tree.links.new(returnMater.node_tree.nodes['Diffuse BSDF'].outputs[0],
                                    returnMater.node_tree.nodes['Mix Shader'].inputs[1])
    returnMater.node_tree.links.new(returnMater.node_tree.nodes['Glossy BSDF'].outputs[0],
                                    returnMater.node_tree.nodes['Mix Shader'].inputs[2])
    returnMater.node_tree.links.new(returnMater.node_tree.nodes['Mix Shader'].outputs[0],
                                    returnMater.node_tree.nodes['Material Output'].inputs[0])
    return returnMater

# Create a list of atomic materials
atomicMaters = []
for i in range(len(atomicColors)):
    atomicMaters += [makeMaterial("Atom Material "+str(i),atomicColors[i])]

# Read an input file
atomFile = open("/Users/23b/Documents/BlenderScripts/input_charge.xyz")
numAtoms = int(atomFile.readline())
numBonds = int(atomFile.readline())
numHydBonds = int(atomFile.readline())
atomFile.readline() # Skip the structure name

for atomNum in range(numAtoms):
    nextLine = atomFile.readline().split("\t")
    print(nextLine)
    atomList += [(nextLine[0], float(nextLine[1]), float(nextLine[2]), float(nextLine[3]))]
    # Step 1, set the cursor location
    bpy.context.scene.cursor_location = (float(nextLine[1]),
            float(nextLine[2]), float(nextLine[3]))

    # Step 2, create the sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, size=0.1)
    # Save a reference to the newly created atom.
    nextAtom = bpy.context.active_object

    # Step 3, add appropriate modifiers and materials
    nextAtom.modifiers.new(type="SUBSURF", name="Subsurf")
    nextAtom.modifiers['Subsurf'].render_levels = 4
    nextAtom.data.materials.append(atomicMaters[int(nextLine[0])])
print("Imported Atoms")

# Mesh editor
# meshEdit = bmesh.new()

for bondNum in range(numBonds):
    # Includes Atom 1, Atom 2, position 1x, 1y, 1z, position 2x, 2y, 2z
    nextLine = atomFile.readline().split("\t")
    print(nextLine)
    atom1 = atomList[int(nextLine[0])-1]
    atom2 = atomList[int(nextLine[1])-1]
    delX = (atom1[1] - atom2[1]) / 2
    delY = (atom1[2] - atom2[2]) / 2
    delZ = (atom1[3] - atom2[3]) / 2
    aveX = (atom1[1] + atom2[1]) / 2
    aveY = (atom1[2] + atom2[2]) / 2
    aveZ = (atom1[3] + atom2[3]) / 2
    # Split into two cylinders for multi-color bonds
    # Create the first cylinder
    x1 = aveX + delX/2
    y1 = aveY + delY/2
    z1 = aveZ + delZ/2
    bondLength = math.sqrt(delX**2 + delY**2 + delZ**2)
    Rx = math.acos(delZ / math.sqrt(delX**2+delY**2+delZ**2))
    Rz = math.atan2(delY,delX) + math.pi/2
    # Step 1 create cylinder
    bpy.context.scene.cursor_location = (x1, y1, z1)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=bondRadius, depth=bondLength, rotation=(Rx,0,Rz))
    nextBond = bpy.context.active_object
    # Step 2 remove the endcaps
    meshEdit = bmesh.new()
    meshEdit.from_mesh(nextBond.data)
    for face in meshEdit.faces:
        if len(face.verts) > 4:
            meshEdit.faces.remove(face)
    meshEdit.to_mesh(nextBond.data)
    meshEdit.free()
    # Step 3, add appropriate modifiers and materials
    nextBond.modifiers.new(type="SUBSURF", name="Subsurf")
    nextBond.modifiers['Subsurf'].render_levels = 4
    nextBond.data.materials.append(atomicMaters[int(atom1[0])])
    # Create the second cylinder
    x2 = aveX - delX/2
    y2 = aveY - delY/2
    z2 = aveZ - delZ/2
    bondLength = math.sqrt(delX**2 + delY**2 + delZ**2)
    Rx = math.acos(delZ / math.sqrt(delX**2+delY**2+delZ**2))
    Rz = math.atan2(delY,delX) + math.pi/2
    # Step 1 create cylinder
    bpy.context.scene.cursor_location = (x2, y2, z2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=bondRadius, depth=bondLength, rotation=(Rx,0,Rz))
    nextBond = bpy.context.active_object
    # Step 2 remove the endcaps
    meshEdit = bmesh.new()
    meshEdit.from_mesh(nextBond.data)
    for face in meshEdit.faces:
        if len(face.verts) > 4:
            meshEdit.faces.remove(face)
    meshEdit.to_mesh(nextBond.data)
    meshEdit.free()
    # Step 3, add appropriate modifiers and materials
    nextBond.modifiers.new(type="SUBSURF", name="Subsurf")
    nextBond.modifiers['Subsurf'].render_levels = 4
    nextBond.data.materials.append(atomicMaters[int(atom2[0])])
print("Imported Bonds")

# Create visuals for the series of hydrogen bonds
for bondNum in range(numHydBonds):
    # Includes Atom 1, Atom 2
    nextLine = atomFile.readline().split("\t")
    print(nextLine)
    atom1 = atomList[int(nextLine[0])]
    atom2 = atomList[int(nextLine[1])]
    delX = (atom1[1] - atom2[1])
    delY = (atom1[2] - atom2[2])
    delZ = (atom1[3] - atom2[3])
    startX = atom2[1]
    startY = atom2[2]
    startZ = atom2[3]
    length = math.sqrt(delX**2 + delY**2 + delZ**2)
    numSteps = int(length / hydBondSpacing)
    for step in range(numSteps-1):
        xPos = startX + delX*(step+1)/numSteps
        yPos = startY + delY*(step+1)/numSteps
        zPos = startZ + delZ*(step+1)/numSteps
        bpy.context.scene.cursor_location = (xPos, yPos, zPos)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=hydBondSegs, ring_count=hydBondSegs, size=hydBondRadius)
        nextBond = bpy.context.active_object
        nextBond.modifiers.new(type="SUBSURF", name="Subsurf")
        nextBond.modifiers['Subsurf'].render_levels = 4
        nextBond.data.materials.append(atomicMaters[4])
print("Imported Hydrogen Bonds")
