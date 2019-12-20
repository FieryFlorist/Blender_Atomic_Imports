# Blender_Atomic_Imports

This folder currently contains the following four scripts:
ImportPolymerScript.py
A simple script that reads atomic sites from a .xyz file, then creates spheres at the appropriate locations in Blender.

ImportPolymerScript_WithBond.py
A script that imports atoms at given xyz locations, then creates covalent bonds between the listed pairs of atoms, then creates dotted hydrogen-bonds between the listed pairs of atoms. NOTE: the dotted hydrogen bonds are simulated as a line of spheres. Long hydrogen bonds require a large number of spheres, which can be taxing on your computer.

ImportPolymerScript_ChargeColors.py
The same basic script as the script above, but atomic colors are set based on imported net charge values, not atom type.

createTetra.py
A script that reads in tetrahedra as a collection of four vertices, then creates those tetrahedra in Blender.
