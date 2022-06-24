from MainPackage import *
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw
import OpenGL
import math

from MainPackage.Objects import Object

windowManager = Window.WindowManager(1280, 720, "Main")
windowManager.show()

shader = Shader.Shader(3)


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

while windowManager.loop():
    windowManager.clear()

    heli_helice.rotate(0, 20, 0)
    heli_helice2.rotate(20, 0, 0)

    # Drawing Objects
    shader.draw_object(heli_base)
    shader.draw_object(heli_helice)
    shader.draw_object(heli_helice2)
    shader.draw_object(base)

    #Drawing Lights (Max of 5 slots, hard coded into fragment shader)
    shader.draw_light(light_1, 0)

    windowManager.update(shader.get_program())

Window.WindowManager.terminate()