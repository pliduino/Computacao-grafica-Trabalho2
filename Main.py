from MainPackage import *
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw
import OpenGL

windowManager = Window.WindowManager(1280, 720, "Main")
windowManager.show()

shader = Shader.Shader(3)


base = Objects.MeshObject()
base.load_mesh_file("Meshes/SM_Terreno.obj")
base.set_texture(shader.load_texture("Textures/T_Pedra.jpg"))
base.set_scale(20, 20, 20)

shader.bind_mesh(base)
shader.upload_binded_meshes()

print(base)
print("\n")
print(shader._vertices_list)

while windowManager.loop():
    windowManager.clear()
    base.rotate(0, .1, 0)
    # Drawing Objects
    shader.draw_object(base)
    

    windowManager.update(shader.get_program())
    

Window.WindowManager.terminate()