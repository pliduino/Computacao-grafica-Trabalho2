import math
import glm

class Camera():
    def __init__(self):
        self.pos   = glm.vec3(0.0,  4.0,  1.0);
        self.front = glm.vec3(0.0,  0.0, -1.0);
        self.up    = glm.vec3(0.0,  1.0,  0.0);

    def get_front(self):
        front = glm.vec3(self.front.x, self.front.y, self.front.z)
        #front = glm.normalize(front)
        return front

    def get_side(self):
        return glm.normalize(glm.cross(self.front, self.up))

    def set_rotation(self, yaw, pitch):
        front = glm.vec3()
        front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
        front.y = math.sin(glm.radians(pitch))
        front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
        
        self.front = glm.normalize(front)
