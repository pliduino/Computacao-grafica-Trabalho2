from MainPackage import *
from OpenGL.GL import *
import OpenGL.GL.shaders
import glfw
import OpenGL

windowManager = Window.WindowManager(1280, 720, "Main")
windowManager.show()

shader = Shader.Shader(1)


base = Objects.MeshObject()
base.load_mesh_file("Meshes/SM_Terreno.obj")
base.set_texture(shader.load_texture("Textures/T_Pedra.jpg"))

shader.bind_mesh(base)
shader.upload_binded_meshes()

print(base)

while windowManager.loop():
    windowManager.clear()
    
    # Drawing Objects
    shader.draw_object(base)
    

    windowManager.update(shader.get_program())
    

Window.WindowManager.terminate()