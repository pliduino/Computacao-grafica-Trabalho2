import MainPackage.Camera as Camera
import MainPackage.Object as Object
import MainPackage.Window as Window
import glfw

window = Window.WindowManager(1280, 720, "Main")

window.show()

while window.loop:

    Window.WindowManager.terminate()