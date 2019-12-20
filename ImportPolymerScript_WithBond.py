import bpy
import bmesh
import math

scale = 0.1

# Carbon, Hydrogen, Nitrogen
atomicRadii = [0.1, 0.1, 0.1, 0.1]
# Carbon, Hydrogen, Nitrogen, Oxygen
atomicColors = [(0.131, 0.067, 0.017, 1.0),
                (0.630, 0.500, 0.500, 1.0),
                (0.055, 0.181, 0.016, 1.0),
				(0.377, 0.000, 0.002, 1.0) ]
bondRadius = 0.1
hydBondSpacing = 0.2
hydBondRadius = 0.05
hydBondSegs = 6
atomList = []

# Create the appropriate materials
# Loop through the materials, so I don't re-define materials that already exist
materCarbon = False
materHydrogen = False
materNitrogen = False
materOxygen = False
for material in bpy.data.materials:
    if material.name == 'CarbonAtom':
        materCarbon = material
    if material.name == 'HydrogenAtom':
        materHydrogen = material
    if material.name == 'NitrogenAtom':
        materNitrogen = material
    if material.name == 'OxygenAtom':
        materOxygen = material

# Create Carbon Material
if materCarbon == False:
    materCarbon = bpy.data.materials.new(name="CarbonAtom")
    materCarbon.use_nodes = True
    materCarbon.diffuse_color = atomicColors[0][:3]
    # Create Shaders
    materCarbon.node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = atomicColors[0]
    materCarbon.node_tree.nodes['Diffuse BSDF'].inputs[1].default_value = 1.0
    materCarbon.node_tree.nodes.new(type="ShaderNodeBsdfGlossy") # "Glossy BSDF"
    materCarbon.node_tree.nodes['Glossy BSDF'].inputs[0].default_value = atomicColors[0]
    materCarbon.node_tree.nodes['Glossy BSDF'].inputs[1].default_value = 0.15
    materCarbon.node_tree.nodes.new(type="ShaderNodeMixShader") # "Mix Shader"
    materCarbon.node_tree.nodes['Mix Shader'].inputs[0].default_value = 0.1
    # Link Shaders
    materCarbon.node_tree.links.remove(materCarbon.node_tree.links[0])
    materCarbon.node_tree.links.new(materCarbon.node_tree.nodes['Diffuse BSDF'].outputs[0],
                                    materCarbon.node_tree.nodes['Mix Shader'].inputs[1])
    materCarbon.node_tree.links.new(materCarbon.node_tree.nodes['Glossy BSDF'].outputs[0],
                                    materCarbon.node_tree.nodes['Mix Shader'].inputs[2])
    materCarbon.node_tree.links.new(materCarbon.node_tree.nodes['Mix Shader'].outputs[0],
                                    materCarbon.node_tree.nodes['Material Output'].inputs[0])

# Create Hydrogen Material
if materHydrogen == False:
    materHydrogen = bpy.data.materials.new(name="HydrogenAtom")
    materHydrogen.use_nodes = True
    materHydrogen.diffuse_color = atomicColors[1][:3]
    # Create Shaders
    materHydrogen.node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = atomicColors[1]
    materHydrogen.node_tree.nodes['Diffuse BSDF'].inputs[1].default_value = 1.0
    materHydrogen.node_tree.nodes.new(type="ShaderNodeBsdfGlossy") # "Glossy BSDF"
    materHydrogen.node_tree.nodes['Glossy BSDF'].inputs[0].default_value = atomicColors[1]
    materHydrogen.node_tree.nodes['Glossy BSDF'].inputs[1].default_value = 0.15
    materHydrogen.node_tree.nodes.new(type="ShaderNodeMixShader") # "Mix Shader"
    materHydrogen.node_tree.nodes['Mix Shader'].inputs[0].default_value = 0.1
    # Link Shaders
    materHydrogen.node_tree.links.remove(materHydrogen.node_tree.links[0])
    materHydrogen.node_tree.links.new(materHydrogen.node_tree.nodes['Diffuse BSDF'].outputs[0],
                                    materHydrogen.node_tree.nodes['Mix Shader'].inputs[1])
    materHydrogen.node_tree.links.new(materHydrogen.node_tree.nodes['Glossy BSDF'].outputs[0],
                                    materHydrogen.node_tree.nodes['Mix Shader'].inputs[2])
    materHydrogen.node_tree.links.new(materHydrogen.node_tree.nodes['Mix Shader'].outputs[0],
                                    materHydrogen.node_tree.nodes['Material Output'].inputs[0])

# Create Nitrogen Material
if materNitrogen == False:
    materNitrogen = bpy.data.materials.new(name="NitrogenAtom")
    materNitrogen.use_nodes = True
    materNitrogen.diffuse_color = atomicColors[2][:3]
    # Create Shader
    materNitrogen.node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = atomicColors[2]
    materNitrogen.node_tree.nodes['Diffuse BSDF'].inputs[1].default_value = 1.0
    materNitrogen.node_tree.nodes.new(type="ShaderNodeBsdfGlossy") # "Glossy BSDF"
    materNitrogen.node_tree.nodes['Glossy BSDF'].inputs[0].default_value = atomicColors[2]
    materNitrogen.node_tree.nodes['Glossy BSDF'].inputs[1].default_value = 0.15
    materNitrogen.node_tree.nodes.new(type="ShaderNodeMixShader") # "Mix Shader"
    materNitrogen.node_tree.nodes['Mix Shader'].inputs[0].default_value = 0.1
    # Link Shaders
    materNitrogen.node_tree.links.remove(materNitrogen.node_tree.links[0])
    materNitrogen.node_tree.links.new(materNitrogen.node_tree.nodes['Diffuse BSDF'].outputs[0],
                                    materNitrogen.node_tree.nodes['Mix Shader'].inputs[1])
    materNitrogen.node_tree.links.new(materNitrogen.node_tree.nodes['Glossy BSDF'].outputs[0],
                                    materNitrogen.node_tree.nodes['Mix Shader'].inputs[2])
    materNitrogen.node_tree.links.new(materNitrogen.node_tree.nodes['Mix Shader'].outputs[0],
                                    materNitrogen.node_tree.nodes['Material Output'].inputs[0])

# Create Oxygen Material
if materOxygen == False:
    materOxygen = bpy.data.materials.new(name="OxygenAtom")
    materOxygen.use_nodes = True
    materOxygen.diffuse_color = atomicColors[3][:3]
    # Create Shader
    materOxygen.node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = atomicColors[3]
    materOxygen.node_tree.nodes['Diffuse BSDF'].inputs[1].default_value = 1.0
    materOxygen.node_tree.nodes.new(type="ShaderNodeBsdfGlossy") # "Glossy BSDF"
    materOxygen.node_tree.nodes['Glossy BSDF'].inputs[0].default_value = atomicColors[3]
    materOxygen.node_tree.nodes['Glossy BSDF'].inputs[1].default_value = 0.15
    materOxygen.node_tree.nodes.new(type="ShaderNodeMixShader") # "Mix Shader"
    materOxygen.node_tree.nodes['Mix Shader'].inputs[0].default_value = 0.1
    # Link Shaders
    materOxygen.node_tree.links.remove(materOxygen.node_tree.links[0])
    materOxygen.node_tree.links.new(materOxygen.node_tree.nodes['Diffuse BSDF'].outputs[0],
                                    materOxygen.node_tree.nodes['Mix Shader'].inputs[1])
    materOxygen.node_tree.links.new(materOxygen.node_tree.nodes['Glossy BSDF'].outputs[0],
                                    materOxygen.node_tree.nodes['Mix Shader'].inputs[2])
    materOxygen.node_tree.links.new(materOxygen.node_tree.nodes['Mix Shader'].outputs[0],
                                    materOxygen.node_tree.nodes['Material Output'].inputs[0])

# Read an input file
atomFile = open("/Users/23b/Documents/BlenderScripts/input.xyz")
numAtoms = int(atomFile.readline())
numBonds = int(atomFile.readline())
numHydBonds = int(atomFile.readline())
atomFile.readline() # Skip the structure name

for atomNum in range(numAtoms):
    nextLine = atomFile.readline().split("\t")
    print(nextLine)
    atomList += [(nextLine[0], float(nextLine[1]), float(nextLine[2]), float(nextLine[3]))]
    # Step 1, set the cursor location
    bpy.context.scene.cursor_location = (scale*float(nextLine[1]),
            scale*float(nextLine[2]), scale*float(nextLine[3]))

    # Step 2, create the sphere
    if nextLine[0] == "C":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, size=scale*atomicRadii[0])
    if nextLine[0] == "H":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, size=scale*atomicRadii[1])
    if nextLine[0] == "N":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, size=scale*atomicRadii[2])
    if nextLine[0] == "N":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, size=scale*atomicRadii[3])
    # Save a reference to the newly created atom.
    nextAtom = bpy.context.active_object

    # Step 3, add appropriate modifiers and materials
    nextAtom.modifiers.new(type="SUBSURF", name="Subsurf")
    nextAtom.modifiers['Subsurf'].render_levels = 4
    if nextLine[0] == "C":
        nextAtom.data.materials.append(materCarbon)
    if nextLine[0] == "H":
        nextAtom.data.materials.append(materHydrogen)
    if nextLine[0] == "N":
        nextAtom.data.materials.append(materNitrogen)
    if nextLine[0] == "O":
        nextAtom.data.materials.append(materOxygen)
print("Imported Atoms")

# Mesh editor
# meshEdit = bmesh.new()

for bondNum in range(numBonds):
    # Includes Atom 1, Atom 2, position 1x, 1y, 1z, position 2x, 2y, 2z
    nextLine = atomFile.readline().split("\t")
    print(nextLine)
    atom1 = atomList[int(nextLine[0])-1]
    atom2 = atomList[int(nextLine[1])-1]
    delX = scale * (atom1[1] - atom2[1]) / 2
    delY = scale * (atom1[2] - atom2[2]) / 2
    delZ = scale * (atom1[3] - atom2[3]) / 2
    aveX = scale * (atom1[1] + atom2[1]) / 2
    aveY = scale * (atom1[2] + atom2[2]) / 2
    aveZ = scale * (atom1[3] + atom2[3]) / 2
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
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=scale*bondRadius, depth=bondLength, rotation=(Rx,0,Rz))
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
    if atom1[0] == "C":
        nextBond.data.materials.append(materCarbon)
    if atom1[0] == "H":
        nextBond.data.materials.append(materHydrogen)
    if atom1[0] == "N":
        nextBond.data.materials.append(materNitrogen)
    if atom1[0] == "O":
        nextBond.data.materials.append(materOxygen)
    # Create the second cylinder
    x2 = aveX - delX/2
    y2 = aveY - delY/2
    z2 = aveZ - delZ/2
    bondLength = math.sqrt(delX**2 + delY**2 + delZ**2)
    Rx = math.acos(delZ / math.sqrt(delX**2+delY**2+delZ**2))
    Rz = math.atan2(delY,delX) + math.pi/2
    # Step 1 create cylinder
    bpy.context.scene.cursor_location = (x2, y2, z2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=scale*bondRadius, depth=bondLength, rotation=(Rx,0,Rz))
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
    if atom2[0] == "C":
        nextBond.data.materials.append(materCarbon)
    if atom2[0] == "H":
        nextBond.data.materials.append(materHydrogen)
    if atom2[0] == "N":
        nextBond.data.materials.append(materNitrogen)
    if atom2[0] == "O":
        nextBond.data.materials.append(materOxygen)
print("Imported Bonds")

# Create visuals for the series of hydrogen bonds
for bondNum in range(numHydBonds):
    # Includes Atom 1, Atom 2
    nextLine = atomFile.readline().split("\t")
    print(nextLine)
    atom1 = atomList[int(nextLine[0])]
    atom2 = atomList[int(nextLine[1])]
    delX = scale * (atom1[1] - atom2[1])
    delY = scale * (atom1[2] - atom2[2])
    delZ = scale * (atom1[3] - atom2[3])
    startX = scale * atom2[1]
    startY = scale * atom2[2]
    startZ = scale * atom2[3]
    length = math.sqrt(delX**2 + delY**2 + delZ**2)
    numSteps = int(length / (scale * hydBondSpacing))
    for step in range(numSteps-1):
        xPos = startX + delX*(step+1)/numSteps
        yPos = startY + delY*(step+1)/numSteps
        zPos = startZ + delZ*(step+1)/numSteps
        bpy.context.scene.cursor_location = (xPos, yPos, zPos)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=hydBondSegs, ring_count=hydBondSegs, size=scale*hydBondRadius)
        nextBond = bpy.context.active_object
        nextBond.modifiers.new(type="SUBSURF", name="Subsurf")
        nextBond.modifiers['Subsurf'].render_levels = 4
        nextBond.data.materials.append(materHydrogen)
print("Imported Hydrogen Bonds")

