# Sorcar

Procedural modeling in Blender using Node Editor

![sc_cover](https://user-images.githubusercontent.com/26548023/68349507-651b6a00-0123-11ea-9769-a01744cc7084.png "Sorcar v3")
<!-- [![alt text](http://img.youtube.com/vi/VIDEO_ID/0.jpg)](http://www.youtube.com/watch?v=VIDEO_ID "Sorcar v3") -->
</br>Github: <https://github.com/aachman98/Sorcar>
</br>BlenderArtist Thread: <https://blenderartists.org/t/sorcar-formerly-procgenmod-procedural-modeling-in-blender-using-node-editor/1156769>
</br>Intro & Tutorials: <https://www.youtube.com/playlist?list=PLZiIC3gdS_O7nCm1-xpWbZmTQWeL5c6KV>
<!-- </br>Itch: <> -->
<!-- </br>Gumroad: <> -->
</br>Trello (Project Tracker): <https://trello.com/b/aKIFRoTh/sorcar-v205>

## About

Sorcar is a **procedural modeling node-based system** which utilises Blender and its Python API to create a visual programming environment for artists and developers. Heavily inspired by Side-FX Houdini, it presents a node editor with a variety of **modular nodes** to make the modelling workflow easier and fast. Most of the nodes are blender internal operations (bpy.ops.mesh/object) which also makes it easier for frequent blender users to manipulate geometry. It helps the users to quickly create 3D models and **control node parameters** to generate limitless variations in a **non-destructive** manner. It also provides the users to view and edit mesh on any stage of the node network independently, with **realtime updates**.

## Release & Instructions

<!-- Latest Release (v3.1.0): <https://github.com> -->
</br>*Requirement: Blender 2.80 or later*

1. Download the zip file and install it as a Blender addon (Edit -> Preferences... -> Add-ons-> Install...)
2. Open Sorcar Node Editor (**Do not** remove the 3D viewport as it is required by some operations like extrude, transform, ...)
3. Click on the + button to create a new tree
4. Press Shift+A to open the nodes menu. Alternatively, navigate through tabs on the Right panel in the node editor
5. Select the desired node and press "Set Preview"

*Open blender using a command prompt to view logs and errors, if encountered.*

## Features

| | |
| --- | --- |
| ![alt text](http://randallmfg.com/ramps/wp-content/uploads/2013/02/640x480.jpg "Visual Programming") | <p style="text-align: left; padding-left: 16px;"><strong>VISUAL PROGRAMMING</strong><br /><em>Don't like programming?</em></p> <hr style="padding-left: 16px;" /> <p style="text-align: left; padding-left: 16px;">Construct geometries using custom algorithms, maths or generate patterns without writing a single line of code!</p> |
| <p style="text-align: right; padding-right: 16px;"><strong>NON-DESTRUCTIVE WORKFLOW</strong><br /><em>Want to change cylinder vertices after bevel?</em></p> <hr style="padding-right: 16px;" /> <p style="text-align: right; padding-right: 16px;">Edit node parameters at any point without the fear of losing mesh data. Also apply same procedural operations to different objects easily.</p> | ![alt text](http://randallmfg.com/ramps/wp-content/uploads/2013/02/640x480.jpg "Non-Destructive Workflow") |
| ![alt text](http://randallmfg.com/ramps/wp-content/uploads/2013/02/640x480.jpg "Realtime Updates") | <p style="text-align: left; padding-left: 16px;"><strong>REAL-TIME UPDATES</strong><br /><em>Quick as the wind...</em></p> <hr style="padding-left: 16px;" /> <p style="text-align: left; padding-left: 16px;">Drive a parameter using current frame value (or manually change it) and see the mesh update in viewport.</p> |
| <p style="text-align: right; padding-right: 16px;"><strong>ITERATE & RANDOMIZE</strong><br /><em>Need multiple extrusions of random amount?</em></p> <hr style="padding-right: 16px;" /> <p style="text-align: right; padding-right: 16px;">Generate variations in mesh by using seed-controlled pseudorandom numbers. Use loops to handle repeatitive operations with same level of randomness.</p> | ![alt text](http://randallmfg.com/ramps/wp-content/uploads/2013/02/640x480.jpg "Iterate & Randomize") |
| ![alt text](http://randallmfg.com/ramps/wp-content/uploads/2013/02/640x480.jpg "Automation") | <p style="text-align: left; padding-left: 16px;"><strong>AUTOMATION</strong><br /><em>Modify, Save, Repeat...</em></p> <hr style="padding-left: 16px;" /> <p style="text-align: left; padding-left: 16px;">Use frame number to drive seed value and batch export the meshes in different files.</p> |
| <p style="text-align: right; padding-right: 16px;"><strong>170+ NODES</strong><br /><em>At your service!</em></p> <hr style="padding-right: 16px;" /> <p style="text-align: right; padding-right: 16px;">A growing list of functions available as nodes (operators & scene settings) including custom inputs, selection & transform tools, modifiers and component level operators.</p> | ![alt text](http://randallmfg.com/ramps/wp-content/uploads/2013/02/640x480.jpg "170+ Nodes") |

- Simplified node sockets with internal data conversion for the convenience of users.
- Colour-coded nodes (preview, error, invalid inputs etc.) for easier debugging.
- Multi-level heirarchy & auto-registration of classes for easy development of custom nodes in any category (existing or new).

and more...!

## Nodes

| | |
| --- | --- |
| ![sc_inputs](https://user-images.githubusercontent.com/26548023/68349488-5f258900-0123-11ea-9836-eeebd36c0247.png "Inputs") | **Inputs** </br> Primitive Meshes (Cube, Cylinder, Sphere, ...), Import FBX, Custom Object from the scene |
| ![sc_transform](https://user-images.githubusercontent.com/26548023/68349489-5f258900-0123-11ea-815e-31250963a9ae.png "Transform") | **Transform** </br> Set/Add/Randomize transform (Edit/Object mode), Apply transform, Create custom orientation|
| ![sc_selection](https://user-images.githubusercontent.com/26548023/68349490-5f258900-0123-11ea-812a-442c09716f9e.png "Selection") | **Selection** </br> Manual, invert/toggle, loops, random, similar components or by their property (location, index, normal, material, ...) |
| ![sc_deletion](https://user-images.githubusercontent.com/26548023/68349492-5fbe1f80-0123-11ea-8d37-2d214eb3f6be.png "Deletion") | **Deletion** </br> Delete/Dissolve selected components (or loops) |
| | |
| ![sc_component_operators](https://user-images.githubusercontent.com/26548023/68349493-5fbe1f80-0123-11ea-85f3-40d2941c9b26.png "Component Operators") | **Component Operators** </br> Bevel, Decimate, Extrude, Fill, Inset, Loop Cut, Merge, Offset Loop, Poke, Screw, Spin, Subdivide, UV Map |
| ![sc_object_operators](https://user-images.githubusercontent.com/26548023/68349494-5fbe1f80-0123-11ea-9627-d026c49b014f.png "Object Operators") | **Object Operators** </br> Duplicate, Raycast/Overlap, Merge, Scatter, Shading, Viewport Draw Mode |
| ![sc_modifiers](https://user-images.githubusercontent.com/26548023/68349495-6056b600-0123-11ea-91d4-8376f86fd12b.png "Modifiers") | **Modifiers** </br> Array, Bevel, Boolean, Build, Cast, Curve, Decimate, Remesh, Skin, Solidify, Subsurf, Wave, Wireframe |
| | |
| ![sc_constants](https://user-images.githubusercontent.com/26548023/68349497-6056b600-0123-11ea-8e14-4ace0ce6312c.png "Constants") | **Constants** </br> Number (Float/Int/Angle/Random), Bool, Vector, String |
| ![sc_utilities](https://user-images.githubusercontent.com/26548023/68349498-6056b600-0123-11ea-9677-28494c38dec1.png "Utilities") | **Utilities** </br> Array, String/Bool/Vector ops, Maths, Clamp, Map, Trigonometry, Scene/Component/Object Info, Custom Python Script |
| ![sc_flow_control](https://user-images.githubusercontent.com/26548023/68349500-60ef4c80-0123-11ea-9437-01ee457a85c5.png "Flow Control") | **Flow Control** </br> For loop, For-Each loop, If-Else Branch |
| ![sc_settings](https://user-images.githubusercontent.com/26548023/68349487-5e8cf280-0123-11ea-9e7b-19466fdeb856.png "Settings") | **Settings** </br> Cursor Transform, Edit Mode, Pivot Point, Transform Orientation |

## Upcoming Feature

1. Update addon using CGCookie Addon Updater module (<https://github.com/CGCookie/blender-addon-updater)>
2. Improve loop nodes: Add more options to control in each pass
3. Curve nodes: Edit spline properties, convert to mesh
4. More array operations: Add/append, remove, push/pop, find, count
5. Named variables: Get/set values of custom variables, accessible across node trees

## Future

1. Node Groups: Collapse big node networks into a single node with custom inputs & outputs
2. Complete integration to dependency graph
3. Debugging tools: Watch/track values of node parameters
4. Node-Viewport link: Create nodes automatically in editor based on actions in 3D viewport

## Showcase

![sc_logo](https://raw.githubusercontent.com/aachman98/Sorcar/v3.0-alpha/sorcar.png "Sorcar")
![sc_showcase](https://user-images.githubusercontent.com/26548023/68349644-de1ac180-0123-11ea-8ba0-9d0da373c9fd.jpg "Made in Sorcar")
