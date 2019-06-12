# Sorcar (formerly ProcGenMod)
Procedural modeling in Blender using Node Editor (Latest version: v2.0.4)
![alt text](https://github.com/aachman98/Sorcar/raw/master/sorcar.png "Sorcar in action")

Introduction Video: https://www.youtube.com/watch?v=nKEeGVtGdlk (outdated)

Tutorials & Feature showcase: https://www.youtube.com/playlist?list=PLZiIC3gdS_O4bXF1cN6T68coTcOUzZOjW (old system - v1.0)

BlenderArtist thread: https://blenderartists.org/t/procgenmod-procedural-modeling-in-blender-using-node-editor/1156769

Progress tracker (Trello): https://trello.com/b/aKIFRoTh

## About
Sorcar (formerly ProcGenMod) is a procedural modeling node-based system which utilises Blender and its Python API to create a visual programming environment for artists and developers. Heavily inspired by Side-FX Houdini, it presents a node editor with a variety of modular nodes to make the workflow easier and fast. Most of the nodes are blender internal operations (bpy.ops.mesh) which also makes it easier for frequent blender users to manipulate geometry. It helps the users to quickly create 3D models and control node parameters to generate limitless variations in a non-destructive manner. It also provides the users to view and edit mesh on any stage of the node network independently, with realtime updates.

## Instructions 
1. Download the zip file and install it as a Blender addon (User preferences -> Install addon from file...)

_NOTE: Built and tested only for Blender 2.79b_

2. Open Node Editor (__Do not__ remove the 3D viewport as it is required by some operations like extrude, transform, ...)
3. Navigate to "Sorcar" node tree and create a new one
4. (Optional) Search for "Realtime Mesh Update" operator (search hotkey: Spacebar) and run it to enable active node preview. Now selecting any node will change the mesh accordingly.

_NOTE: Re-run the operator if encountered any error/exception. To stop realtime preview, press "ESC"._

5. Press Shift+A to open the nodes menu. Alternatively, navigate through tabs on the left panel in the node editor
6. Add a "Refresh Mesh" node (from the Output category) and select it to display an option to refresh geometry (for cases when not using realtime preview).

Open blender using a command prompt to view degub logs and errors, if encountered.
