import glfw
import Camera
from OpenGL.GL import *
import numpy as np
import glm

class WindowManager:
    has_glfw_init = False

    def __init__(self, width, height, title):
        self._width = width
        self._height = height
        self._title = title
        self._mouse_state = glfw.CURSOR_DISABLED
        self._polygonal_mode = False
        
        # Camera settings
        self.camera = Camera.Camera()
        self.cameraSpeed = 0.35
        self._firstMouse = True
        self._yaw = -90.0 
        self._pitch = 0.0
        self._lastX =  self._width/2
        self._lastY =  self._height/2


        if WindowManager.has_glfw_init == False:
            glfw.init()
            WindowManager.has_glfw_init == True
        
        self.window = glfw.create_window(self._width, self._height, self._title, None, None)
        
        # Hides Cursor
        glfw.set_input_mode(self.window, glfw.CURSOR, self._mouse_state);

        # Binding Events
        glfw.set_key_callback(self.window, self._key_event)
        glfw.set_cursor_pos_callback(self.window, self._mouse_event)

    def show(self):
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
        glfw.make_context_current(self.window)
        glfw.show_window(self.window)

    def loop(self):
        if self._polygonal_mode == True:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        if self._polygonal_mode == False:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        return not glfw.window_should_close(self.window)

    def terminate():
        glfw.terminate()

    def update(self, program):
        mat_view = self._view()
        loc_view = glGetUniformLocation(program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

        mat_projection = self._projection()
        loc_projection = glGetUniformLocation(program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    


        glfw.swap_buffers(self.window)

    def clear(self):
        glfw.poll_events() 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)

    def _view(self):
        mat_view = glm.lookAt(self.camera.pos, self.camera.pos + self.camera.front, self.camera.up);
        mat_view = np.array(mat_view)
        return mat_view

    def _projection(self):
        # perspective parameters: fovy, aspect, near, far
        mat_projection = glm.perspective(glm.radians(75.0), self._width/self._height, 0.1, 1000.0)
        mat_projection = np.array(mat_projection)    
        return mat_projection

    # Input Events
    def _key_event(self, window, key, scancode, action, mods):
        front = self.camera.get_front()

        #Movement Inputs (WASD)
        if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
            self.camera.pos += front * self.cameraSpeed 

        if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
            self.camera.pos -= front * self.cameraSpeed 

        if key == glfw.KEY_A and (action == glfw.PRESS or action == glfw.REPEAT):
            self.camera.pos -= self.camera.get_side() * self.cameraSpeed

        if key == glfw.KEY_D and (action == glfw.PRESS or action == glfw.REPEAT):
            self.camera.pos += self.camera.get_side() * self.cameraSpeed


        if key == glfw.KEY_P and action == 1:
            self._polygonal_mode = not self._polygonal_mode

        # Enable/Disable Cursor
        if key==glfw.KEY_SPACE and action == 1:
            if self._mouse_state == glfw.CURSOR_DISABLED:
                self._mouse_state = glfw.CURSOR_NORMAL
            else:
                self._mouse_state = glfw.CURSOR_DISABLED
            glfw.set_cursor_pos(self.window, self._width, self._height)
            glfw.set_input_mode(window, glfw.CURSOR, self._mouse_state)


    def _mouse_event(self, window, xpos, ypos):
        if self._firstMouse:
            self._lastX = xpos
            self._lastY = ypos
            self._firstMouse = False

        xoffset = xpos - self._lastX
        yoffset = self._lastY - ypos
        self._lastX = xpos
        self._lastY = ypos

        sensitivity = 0.3 
        xoffset *= sensitivity
        yoffset *= sensitivity

        self._yaw += xoffset
        self._pitch += yoffset

        #Limits Pitch
        if self._pitch >= 90.0: 
            self._pitch = 90.0
        if self._pitch <= -90.0: 
            self._pitch = -90.0

        self.camera.set_rotation(self._yaw, self._pitch)