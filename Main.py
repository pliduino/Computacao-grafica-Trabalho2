from MainPackage import *
import glfw

windowManager = Window.WindowManager(1280, 720, "Main")
shader = Shader.Shader(3)

windowManager.show()

while windowManager.loop:
    windowManager.clear()

    # Drawing Objects
    

    windowManager.update(shader.get_program())
    

Window.WindowManager.terminate()