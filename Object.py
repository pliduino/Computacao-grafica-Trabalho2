class Object:
    def __init__(self):
        self._position = {'x': 0, 'y': 0,'z': 0}
        self._rotation = {'x': 0, 'y': 0,'z': 0}
        self._scale = {'x': 1, 'y': 1,'z': 1}

    #Setters
    def set_position(self, x, y, z):
        self._position['x'] = x
        self._position['y'] = y
        self._position['z'] = z
        
    def set_rotation(self, x, y, z):
        self._rotation['x'] = x
        self._rotation['y'] = y
        self._rotation['z'] = z
    
    def set_scale(self, x, y, z):
        self._scale['x'] = x
        self._scale['y'] = y
        self._scale['z'] = z


    #Getters
    def get_position(self):
        return self._position
    
    def get_rotation(self):
        return self._rotation
    
    def get_scale(self):
        return self._scale

class MeshObject(Object):

    def __init__():
        super().__init__()
        