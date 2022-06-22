from OpenGL.GL import *
from PIL import Image
import Objects
import numpy as np
class Shader:
    # Used to set unique IDs to each texture
    

    def __init__(self, n_textures=1):
        self.current_texture_id = 0
        self.vertices_list = []    
        self.textures_coord_list = []
        
        vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        varying vec2 out_texture;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
        }
        """

        fragment_code = """
        uniform vec4 color;
        varying vec2 out_texture;
        uniform sampler2D samplerTexture;
        
        void main(){
            vec4 texture = texture2D(samplerTexture, out_texture);
            gl_FragColor = texture;
        }
        """

        # Requesting a program and shader slots from GPU
        self._program  = glCreateProgram()
        self._vertex   = glCreateShader(GL_VERTEX_SHADER)
        self._fragment = glCreateShader(GL_FRAGMENT_SHADER)
    
        # Setting shaders source
        glShaderSource(self._vertex, vertex_code)
        glShaderSource(self._fragment, fragment_code)
    
        # Compiling shaders
        glCompileShader(self._vertex)
        if not glGetShaderiv(self._vertex, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(self._vertex).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Vertex Shader")

        glCompileShader(self._fragment)
        if not glGetShaderiv(self._fragment, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(self._fragment).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Fragment Shader")

        glAttachShader(self._program, self._vertex)
        glAttachShader(self._program, self._fragment)

        # Build program
        glLinkProgram(self._program)
        if not glGetProgramiv(self._program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self._program))
            raise RuntimeError('Linking error')
            
        # Make program the default program
        glUseProgram(self._program)

        glEnable(GL_DEPTH_TEST) ### importante para 3D
        # Textures
        glEnable(GL_TEXTURE_2D)
        self._n_textures = n_textures
        self.textures = glGenTextures(self._n_textures)

        # Request a buffer slot from GPU
        self._buffer = glGenBuffers(2)

    def get_program(self):
        return self._program
    
    def load_texture(self, filename):
        glBindTexture(GL_TEXTURE_2D, self.current_texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        img = Image.open(filename)
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.tobytes("raw", "RGB", 0, -1)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

        self.current_texture_id += 1
        return self.current_texture_id - 1
    
    def upload_binded_meshes(self):
        #Uploading Vertices
        vertices = np.zeros(len(self.vertices_list), [("position", np.float32, 3)])
        vertices['position'] = self.vertices_list

        glBindBuffer(GL_ARRAY_BUFFER, self._buffer[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(self._program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)
        

        # Uploading Textures
        textures = np.zeros(len(self.textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
        textures['position'] = self._textures_coord_list
        
        glBindBuffer(GL_ARRAY_BUFFER, self._buffer[1])
        glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
        stride = textures.strides[0]
        offset = ctypes.c_void_p(0)
        loc_texture_coord = glGetAttribLocation(self._program, "texture_coord")
        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)

    def draw_object(self, mesh_object: Objects.MeshObject):
        glBindTexture(GL_TEXTURE_2D, mesh_object.texture_id)
        glDrawArrays(GL_TRIANGLES, mesh_object.vertices_index, mesh_object.n_vertices)

    # Loads Object into Shader
    def bind_mesh(self, mesh_object: Objects.MeshObject):
        mesh_object.vertices_index = len(self.vertices_list)

        for face in mesh_object.mesh['faces']:
            for vertice_id in face[0]:
                self.vertices_list.append( mesh_object.mesh['vertices'][vertice_id-1] )
            for texture_id in face[1]:
                self.textures_coord_list.append( mesh_object.mesh['texture'][texture_id-1] )

        #TODO Change n_vertices to be set in load_mesh_file()
        mesh_object.n_vertices = len(self.vertices_list) - mesh_object.vertices_index