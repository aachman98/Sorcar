# Sorcar
Procedural modeling in Blender using Node Editor

![alt text](https://github.com/aachman98/Sorcar/raw/v3.0-alpha/sorcar.png "Sorcar v3 (alpha)")

BlenderArtist thread: https://blenderartists.org/t/procgenmod-procedural-modeling-in-blender-using-node-editor/1156769</br>

## About
Sorcar is a procedural modeling node-based system which utilises Blender and its Python API to create a visual programming environment for artists and developers. Heavily inspired by Side-FX Houdini, it presents a node editor with a variety of modular nodes to make the workflow easier and fast. Most of the nodes are blender internal operations (bpy.ops.mesh) which also makes it easier for frequent blender users to manipulate geometry. It helps the users to quickly create 3D models and control node parameters to generate limitless variations in a non-destructive manner. It also provides the users to view and edit mesh on any stage of the node network independently, with realtime updates.

## Instructions 
1. Download the zip file and install it as a Blender addon (Edit -> Preferences... -> Add-ons-> Install...)

_NOTE: Built and tested only for Blender 2.80_

2. Open Sorcar Node Editor (__Do not__ remove the 3D viewport as it is required by some operations like extrude, transform, ...)
3. Create a new tree
4. Press Shift+A to open the nodes menu. Alternatively, navigate through tabs on the Right panel in the node editor
6. Select the desired node and press "Set Preview"

Open blender using a command prompt to view logs and errors, if encountered.
