import string
import glfw

class Object:

    def __str__(self):
        string_ = "Position: " + self._position.__str__()
        string_ += "\nRotation: " + self._rotation.__str__()
        string_ += "\nScale: " + self._scale.__str__()
        return string_

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


    def rotate(self, x, y, z):
        cur = self.get_rotation()
        self.set_rotation(cur['x'] + x, cur['y'] + y, cur['z'] + z)

class MeshObject(Object):

    def __str__(self):
        string_ = super().__str__()
        string_ += "\n\nMesh: " + self.mesh.__str__()
        string_ += "\n\nTexture ID: " + self.texture_id.__str__()
        string_ += "\nVertice Index: " + self.vertices_index.__str__()
        string_ += "\nVertices: " + self.n_vertices.__str__()
        return string_

    def __init__(self):
        super().__init__()
        self.mesh = {'vertices': None, 'texture': None, 'faces': None}
        self.texture_id = 0

        # Used for rendering at Shader
        self.vertices_index = 0
        self.n_vertices = 0
    
    #Loads a Wavefront OBJ file.
    def load_mesh_file(self, filename):
        vertices = []
        normals = []
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

            
            if values[0] == 'vn':
                normals.append(values[1:4])

            ### recuperando coordenadas de textura
            elif values[0] == 'vt':
                texture_coords.append(values[1:3])

            ### recuperando faces 
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]

            elif values[0] == 'f':
                face = []
                face_texture = []
                face_normals = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    face_normals.append(int(w[2]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, face_normals, material))

        self.mesh = {}
        self.mesh['vertices'] = vertices
        self.mesh['texture'] = texture_coords
        self.mesh['faces'] = faces
        self.mesh['normals'] = normals

    def set_texture(self, texture_id):
        self.texture_id = texture_id