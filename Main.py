from MainPackage import *
import glfw

windowManager = Window.WindowManager(1280, 720, "Main")

windowManager.show()

while windowManager.loop:
    windowManager.clear()

    # Drawing Objects
    

    windowManager.update()
    

Window.WindowManager.terminate()