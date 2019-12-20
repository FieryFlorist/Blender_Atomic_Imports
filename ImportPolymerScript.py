import bpy

# Carbon, Hydrogen, Nitrogen
atomicRadii = [0.3, 0.1, 0.3]
atomicColors = [(0.45, 0.22, 0.05, 1.0),
				(0.80, 0.80, 0.80, 1.0),
				(0.11, 0.38, 0.03, 1.0) ]

# Create the appropriate materials
# Loop through the materials, so I don't re-define materials that already exist
materCarbon = False
materHydrogen = False
materNitrogen = False
for material in bpy.data.materials:
	if material.name == 'CarbonAtom':
		materCarbon = material
	if material.name == 'HydrogenAtom':
		materHydrogen = material
	if material.name == 'NitrogenAtom':
		materNitrogen = material

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

# Read an input file
atomFile = open("/Users/23b/Documents/Structure.xyz")
numAtoms = int(atomFile.readline())
atomFile.readline() # Skip the structure name

for atomNum in range(numAtoms):
	nextLine = atomFile.readline().split(" ")
	# Step 1, set the cursor location
	bpy.context.scene.cursor_location = (float(nextLine[1]),
			float(nextLine[2]), float(nextLine[3]))

	# Step 2, create the sphere
	if nextLine[0] == "C":
		bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, size=atomicRadii[0])
	if nextLine[0] == "H":
		bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, size=atomicRadii[1])
	if nextLine[0] == "N":
		bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, size=atomicRadii[2])
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

