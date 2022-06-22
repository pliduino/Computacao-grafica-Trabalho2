import glfw

class Object:

    def __init__(self, px=0, py=0, pz=0, rx=0, ry=0, rz=0, sx=1, sy=1, sz=1):
        self._position = {'x': px, 'y': py,'z': pz}
        self._rotation = {'x': rx, 'y': ry,'z': rz}
        self._scale = {'x': sx, 'y': sy,'z': sz}

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

    def __init__(self):
        super().__init__()
        self.mesh['vertices'] = None
        self.mesh['texture'] = None
        self.mesh['faces'] = None

    def __init__(self, filename):
        super().__init__()
        self.load_mesh(filename)
    
    #Loads a Wavefront OBJ file.
    def load_mesh(self, filename):
        vertices = []
        texture_coords = []
        faces = []

        material = None

        # Abre o arquivo obj para leitura
        for line in open(filename, "r"): ## para cada linha do arquivo .obj
            if line.startswith('#'): 
                continue ## ignora comentarios
            values = line.split() # quebra a linha por espaço
            if not values: continue


            ### recuperando vertices
            if values[0] == 'v':
                vertices.append(values[1:4])


            ### recuperando coordenadas de textura
            elif values[0] == 'vt':
                texture_coords.append(values[1:3])

            ### recuperando faces 
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]

            elif values[0] == 'f':
                face = []
                face_texture = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, material))

        self.mesh = {}
        self.mesh['vertices'] = vertices
        self.mesh['texture'] = texture_coords
        self.mesh['faces'] = faces