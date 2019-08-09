# Sorcar
Procedural modeling in Blender 2.8 using Node Editor
![alt text](https://github.com/aachman98/Sorcar/raw/master/sorcar.png "Sorcar in action")

Introduction Video: https://www.youtube.com/watch?v=nKEeGVtGdlk (outdated)</br>
Tutorials & Feature showcase: https://www.youtube.com/playlist?list=PLZiIC3gdS_O7nCm1-xpWbZmTQWeL5c6KV</br>
(old system v1 tutorials: https://www.youtube.com/playlist?list=PLZiIC3gdS_O4bXF1cN6T68coTcOUzZOjW)</br>

BlenderArtist thread: https://blenderartists.org/t/procgenmod-procedural-modeling-in-blender-using-node-editor/1156769</br>
Progress tracker (Trello): https://trello.com/b/aKIFRoTh

## About
Sorcar is a procedural modeling node-based system which utilises Blender and its Python API to create a visual programming environment for artists and developers. Heavily inspired by Side-FX Houdini, it presents a node editor with a variety of modular nodes to make the workflow easier and fast. Most of the nodes are blender internal operations (bpy.ops.mesh) which also makes it easier for frequent blender users to manipulate geometry. It helps the users to quickly create 3D models and control node parameters to generate limitless variations in a non-destructive manner. It also provides the users to view and edit mesh on any stage of the node network independently, with realtime updates.

## Instructions 
1. Download the zip file and install it as a Blender addon (Edit -> Preferences -> Add-ons -> Install...)

_NOTE: Partially tested for Blender 2.80_

2. Open Node Editor (__Do not__ remove the 3D viewport as it is required by some operations like extrude, transform, ...)
3. Navigate to "Sorcar" node tree and create a new one
4. (Optional) Search for "Realtime Mesh Update" operator (search hotkey: F3) and run it to enable active node preview. Now selecting any node will change the mesh accordingly.

_NOTE: Re-run the operator if encountered any error/exception. To stop realtime preview, press "ESC"._

5. Press Shift+A to open the nodes menu. Alternatively, navigate through tabs on the right panel in the node editor
6. Add a "Refresh Mesh" node (from the Output category) and select it to display an option to refresh geometry (for cases when not using realtime preview).

Open blender using a command prompt to view degub logs and errors, if encountered.

## Contributors
Mark Andrianov (@SevenNeumann) - Icons for Sorcar & layout design for main menu
</br>Kim Christensen (@kichristensen) - Port Sorcar (v2) to Blender 2.80
