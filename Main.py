from MainPackage import *
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw
import OpenGL
import math

import MainPackage.Objects as Objects
import MainPackage.Window as Window
import MainPackage.Shader as Shader
import MainPackage.Camera as Camera

windowManager = Window.WindowManager(1280, 720, "Main")
windowManager.show()

shader = Shader.Shader(3)

cat = Objects.MeshObject()
cat.load_mesh_file("Meshes/cat1.obj")
cat.set_texture(shader.load_texture("Textures/Cat_diffuse.jpg"))
cat.set_scale(0.3, 0.3, 0.3)
cat.set_rotation(0, 20, 0)
cat.set_position(-10, -5, 0)
shader.bind_mesh(cat)

barril = Objects.MeshObject()
barril.load_mesh_file("Meshes/barril.obj")
barril.set_texture(shader.load_texture("Textures/barril/Wood/Wood Diffuse.jpg"))
barril.set_position(-8, -5, 4)
barril.set_scale(0.8,0.8,0.8)
shader.bind_mesh(barril)

house = Objects.MeshObject()
house.load_mesh_file("Meshes/house.obj")
house.set_texture(shader.load_texture("Textures/teste.jpg"))
house.set_position(0, -5, -10)
shader.bind_mesh(house)

trees = []
for i in range(2):
    tree = Objects.MeshObject()
    tree.load_mesh_file("Meshes/bark.obj")
    tree.set_texture(shader.load_texture("Textures/trees/Bark.jpg"))
    shader.bind_mesh(tree)
    tree.set_position(12, -5, 25 *i-10);
    trees.append(tree)

for i in range(2):
    tree = Objects.MeshObject()
    tree.load_mesh_file("Meshes/bark.obj")
    tree.set_texture(shader.load_texture("Textures/trees/Bark.jpg"))
    shader.bind_mesh(tree)
    tree.set_position(-12, -5, 25 *i-10);
    trees.append(tree)

heli_base = Objects.MeshObject()
heli_base.load_mesh_file("Meshes/low-poly-helicopter_base.obj")
heli_base.set_texture(shader.load_texture("Textures/T_HeliBody.png"))
shader.bind_mesh(heli_base)

heli_helice = Objects.MeshObject()
heli_helice.load_mesh_file("Meshes/low-poly-helicopter_helice.obj")
heli_helice.set_texture(shader.load_texture("Textures/T_Pedra.jpg"))
heli_helice.set_position(0, 1.3, .57)
shader.bind_mesh(heli_helice)

heli_helice2 = Objects.MeshObject()
heli_helice2.load_mesh_file("Meshes/low-poly-helicopter_helice2.obj")
heli_helice2.set_texture(shader.load_texture("Textures/T_Pedra.jpg"))
heli_helice2.set_position(.17, 1.4, -9.1)
shader.bind_mesh(heli_helice2)

base = Objects.MeshObject()
base.load_mesh_file("Meshes/SM_Terreno.obj")
base.set_texture(shader.load_texture("Textures/T_Pedra.jpg"))
base.set_position(0, -5, 0)
base.set_rotation(0, 0, 1)
base.set_scale(20, 20, 20)
shader.bind_mesh(base)

light_1 = Objects.LightObject()

shader.upload_binded_meshes()
heliceSpeed = 10
while windowManager.loop():
    windowManager.clear()

    heli_helice.rotate(0, heliceSpeed, 0)
    heli_helice2.rotate(heliceSpeed, 0, 0)

    # Drawing Objects
    shader.draw_object(heli_base)
    shader.draw_object(heli_helice)
    shader.draw_object(heli_helice2)
    shader.draw_object(base)
    shader.draw_object(cat)
    shader.draw_object(barril)
    for t in trees:
        shader.draw_object(t)
    shader.draw_object(house)
    # Drawing Lights (Max of 5 slots, hard coded into fragment shader)
    shader.draw_light(light_1, 0)

    windowManager.update(shader.get_program())

Window.WindowManager.terminate()
