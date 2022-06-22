import glfw
from OpenGL.GL import *

class WindowManager:
    has_glfw_init = False

    def __init__(self, width, height, title):
        if WindowManager.has_glfw_init == False:
            glfw.init()
            WindowManager.has_glfw_init == True
        self._width = width
        self._height = height
        self._title = title
        self.window = glfw.create_window(self._width, self._height, self._title, None, None)
        
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED);

    def show(self):
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
        glfw.make_context_current(self.window)
        glfw.show_window(self.window)

    def loop(self):
        return not glfw.window_should_close(self.window)

    def terminate():
        glfw.terminate()