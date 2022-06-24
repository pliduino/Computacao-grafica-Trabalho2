from OpenGL.GL import *
from PIL import Image
import Objects
import numpy as np
import glm
import math

class Shader:
    def __init__(self, n_textures=1):
        # Used to set unique IDs to each texture
        self._current_texture_id = 0

        self._vertices_list = []    
        self._textures_coord_list = []
        self.normals_list = []
        
        vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        attribute vec3 normals;

        varying vec2 out_texture;
        varying vec3 out_fragPos;
        varying vec3 out_normal;
            
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
            out_fragPos = vec3(position);
            out_normal = normals;
        }
        """

        fragment_code = """

        uniform vec3 lightPos; // define coordenadas de posicao da luz
        uniform float ka; // coeficiente de reflexao ambiente
        uniform float kd; // coeficiente de reflexao difusa
        
        vec3 lightColor = vec3(1.0, 1.0, 1.0);

        varying vec2 out_texture; // recebido do vertex shader
        varying vec3 out_normal; // recebido do vertex shader
        varying vec3 out_fragPos; // recebido do vertex shader
        uniform sampler2D samplerTexture;
        
        
        
        void main(){
            vec3 ambient = ka * lightColor;             
        
            vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
            vec3 lightDir = normalize(lightPos - out_fragPos); // direcao da luz
            float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
            vec3 diffuse = kd * diff * lightColor; // iluminacao difusa
            
            vec4 texture = texture2D(samplerTexture, out_texture);
            vec4 result = vec4((ambient + diffuse),1.0) * texture; // aplica iluminacao
            gl_FragColor = result;

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


        # Attaching Compiled Shaders
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
        glEnable(GL_LIGHT0)
        self._n_textures = n_textures
        self.textures = glGenTextures(self._n_textures)


        # Request a buffer slot from GPU (Vertices, textures and normals)
        self._buffer = glGenBuffers(3)
        loc_light_pos = glGetUniformLocation(self._program, "lightPos") # recuperando localizacao da variavel lightPos na GPU
        glUniform3f(loc_light_pos, -1.5, 1.7, 2.5) ### posicao da fonte de luz

    def get_program(self):
        return self._program
    
    def load_texture(self, filename):
        glBindTexture(GL_TEXTURE_2D, self._current_texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        img = Image.open(filename)
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.tobytes("raw", "RGB", 0, -1)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
        glMaterial
        self._current_texture_id += 1
        return self._current_texture_id - 1
    
    def upload_binded_meshes(self):
        #Uploading Vertices
        vertices = np.zeros(len(self._vertices_list), [("position", np.float32, 3)])
        vertices['position'] = self._vertices_list

        glBindBuffer(GL_ARRAY_BUFFER, self._buffer[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(self._program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)
        

        # Uploading Textures
        textures = np.zeros(len(self._textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
        textures['position'] = self._textures_coord_list
        
        glBindBuffer(GL_ARRAY_BUFFER, self._buffer[1])
        glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
        stride = textures.strides[0]
        offset = ctypes.c_void_p(0)
        loc_texture_coord = glGetAttribLocation(self._program, "texture_coord")
        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)

        # Uploading Normals
        normals = np.zeros(len(self.normals_list), [("position", np.float32, 3)]) # três coordenadas
        normals['position'] = self.normals_list

        glBindBuffer(GL_ARRAY_BUFFER, self._buffer[2])
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        stride = normals.strides[0]
        offset = ctypes.c_void_p(0)
        loc_normals_coord = glGetAttribLocation(self._program, "normals")
        glEnableVertexAttribArray(loc_normals_coord)
        glVertexAttribPointer(loc_normals_coord, 3, GL_FLOAT, False, stride, offset)

    def draw_object(self, mesh_object: Objects.MeshObject):
        position = mesh_object.get_position()
        rotation = mesh_object.get_rotation()
        scale = mesh_object.get_scale()

        mat_model = Shader._model(rotation['x'], rotation['y'], rotation['z'], 
                            position['x'], position['y'], position['z'], 
                            scale['x'], scale['y'], scale['z'])

        loc_model = glGetUniformLocation(self._program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        
        #TODO Adcionar ka e kd na classe MeshObject
        ka_inc = 0.3
        kd_inc = 0.5

        ka = ka_inc # coeficiente de reflexao ambiente do modelo
        kd = kd_inc # coeficiente de reflexao difusa do modelo

        loc_ka = glGetUniformLocation(self._program, "ka") # recuperando localizacao da variavel ka na GPU
        glUniform1f(loc_ka, ka) ### envia ka pra gpu

        loc_kd = glGetUniformLocation(self._program, "kd") # recuperando localizacao da variavel ka na GPU
        glUniform1f(loc_kd, kd) ### envia kd pra gpu    




        glBindTexture(GL_TEXTURE_2D, mesh_object.texture_id)
        glDrawArrays(GL_TRIANGLES, mesh_object.vertices_index, mesh_object.n_vertices)

    # Loads Object into Shader
    def bind_mesh(self, mesh_object: Objects.MeshObject):
        mesh_object.vertices_index = len(self._vertices_list)

        for face in mesh_object.mesh['faces']:
            for vertice_id in face[0]:
                self._vertices_list.append( mesh_object.mesh['vertices'][vertice_id-1] )
            for texture_id in face[1]:
                self._textures_coord_list.append( mesh_object.mesh['texture'][texture_id-1] )
            for normal_id in face[2]:
                self.normals_list.append(mesh_object.mesh['normals'][normal_id-1] )
        #TODO Change n_vertices to be set in load_mesh_file()
        mesh_object.n_vertices = len(self._vertices_list) - mesh_object.vertices_index

    def _model(r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    
        r_x = math.radians(r_x)
        r_y = math.radians(r_y)
        r_z = math.radians(r_z)

        matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade


        # aplicando translacao
        matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    

        # aplicando rotacao
        matrix_transform = glm.rotate(matrix_transform, r_x, glm.vec3(1, 0, 0))
        matrix_transform = glm.rotate(matrix_transform, r_y, glm.vec3(0, 1, 0))
        matrix_transform = glm.rotate(matrix_transform, r_z, glm.vec3(0, 0, 1))

        # aplicando escala
        matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))

        matrix_transform = np.array(matrix_transform)

        return matrix_transform