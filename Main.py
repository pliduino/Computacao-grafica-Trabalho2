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

heli_helice = Objects.MeshObject()
heli_helice.load_mesh_file("Meshes/low-poly-helicopter_helice.obj")
heli_helice.set_texture(shader.load_texture("Textures/T_Pedra.jpg"))
heli_helice.set_position(0, 1.3, .57)

heli_helice2 = Objects.MeshObject()
heli_helice2.load_mesh_file("Meshes/low-poly-helicopter_helice2.obj")
heli_helice2.set_texture(shader.load_texture("Textures/T_Pedra.jpg"))
heli_helice2.set_position(.17, 1.4, -9.1)

base = Objects.MeshObject()
base.load_mesh_file("Meshes/SM_Terreno.obj")
base.set_texture(shader.load_texture("Textures/T_Pedra.jpg"))
base.set_position(0, -5, 0)
base.set_rotation(0, 0, 1)
base.set_scale(20, 20, 20)

shader.bind_mesh(heli_base)
shader.bind_mesh(heli_helice)
shader.bind_mesh(heli_helice2)
shader.bind_mesh(base)

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

    shader.draw_light("lightPos1", 3, 5, 2)
    shader.draw_light("lightPos2", 3, 5, 2)

    windowManager.update(shader.get_program())
    

Window.WindowManager.terminate()