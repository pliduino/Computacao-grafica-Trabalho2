from OpenGL.GL import *
from PIL import Image
import Objects
import numpy as np
import glm
import math

class Shader:
    ang = 0
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
            out_fragPos = vec3(model * vec4(position, 1.0));
            out_normal = normals;    
        }
        """

        fragment_code = """

        vec3 lightColor = vec3(1.0, 1.0, 1.0);

        vec3 lightColor1 = vec3(1.0, 1.0, 1.0);
        uniform vec3 lightPos1;
        vec3 lightColor2 = vec3(1.0, 1.0, 1.0);
        uniform vec3 lightPos2;

        uniform float ka; // coeficiente de reflexao ambiente
        uniform float kd; // coeficiente de reflexao difusa
        
        uniform vec3 viewPos; // define coordenadas com a posicao da camera/observador
        uniform float ks; // coeficiente de reflexao especular
        uniform float ns; // expoente de reflexao especular

        varying vec2 out_texture; // recebido do vertex shader
        varying vec3 out_normal; // recebido do vertex shader
        varying vec3 out_fragPos; // recebido do vertex shader
        uniform sampler2D samplerTexture;
        
        
        
        void main(){
            vec3 ambient = ka * lightColor;             
        
            // calculando reflexao difusa
            vec3 norm1 = normalize(out_normal); // normaliza vetores perpendiculares
            vec3 lightDir1 = normalize(lightPos1 - out_fragPos); // direcao da luz
            float diff1 = max(dot(norm1, lightDir1), 0.0); // verifica limite angular (entre 0 e 90)
            vec3 diffuse1 = kd * diff1 * lightColor1; // iluminacao difusa
            
            // calculando reflexao especular
            vec3 viewDir1 = normalize(viewPos - out_fragPos); // direcao do observador/camera
            vec3 reflectDir1 = reflect(-lightDir1, norm1); // direcao da reflexao
            float spec1 = pow(max(dot(viewDir1, reflectDir1), 0.0), ns);
            vec3 specular1 = ks * spec1 * lightColor1;   

            // calculando reflexao difusa
            vec3 norm2 = normalize(out_normal); // normaliza vetores perpendiculares
            vec3 lightDir2 = normalize(lightPos2 - out_fragPos); // direcao da luz
            float diff2 = max(dot(norm2, lightDir2), 0.0); // verifica limite angular (entre 0 e 90)
            vec3 diffuse2 = kd * diff2 * lightColor2; // iluminacao difusa
            
            // calculando reflexao especular
            vec3 viewDir2 = normalize(viewPos - out_fragPos); // direcao do observador/camera
            vec3 reflectDir2 = reflect(-lightDir2, norm2); // direcao da reflexao
            float spec2 = pow(max(dot(viewDir2, reflectDir2), 0.0), ns);
            vec3 specular2 = ks * spec2 * lightColor2;                
            
            // aplicando o modelo de iluminacao
            vec4 texture = texture2D(samplerTexture, out_texture);
            vec4 result = vec4((ambient + diffuse1 + diffuse2 + specular1 + specular2),1.0) * texture; // aplica iluminacao
            gl_FragColor = result;

        }
        """

        # Requesting a self._program and shader slots from GPU
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


        # Build self._program
        glLinkProgram(self._program)
        if not glGetProgramiv(self._program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self._program))
            raise RuntimeError('Linking error')
            

        # Make self._program the default self._program
        glUseProgram(self._program)


        glEnable(GL_DEPTH_TEST) ### importante para 3D
        # Textures
        glEnable(GL_TEXTURE_2D)
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


        loc_ka = glGetUniformLocation(self._program, "ka") # recuperando localizacao da variavel ka na GPU
        glUniform1f(loc_ka, mesh_object.ka) ### envia ka pra gpu

        loc_kd = glGetUniformLocation(self._program, "kd") # recuperando localizacao da variavel ka na GPU
        glUniform1f(loc_kd, mesh_object.kd) ### envia kd pra gpu    

        loc_ks = glGetUniformLocation(self._program, "ks") # recuperando localizacao da variavel ks na GPU
        glUniform1f(loc_ks, mesh_object.ks) ### envia ks pra gpu        

        loc_ns = glGetUniformLocation(self._program, "ns") # recuperando localizacao da variavel ns na GPU
        glUniform1f(loc_ns, mesh_object.ns) ### envia ns pra gpu      




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

        mesh_object.n_vertices = len(self._vertices_list) - mesh_object.vertices_index

    def draw_light(self, temp, t_x, t_y, t_z):
        loc_light_pos = glGetUniformLocation(self._program, temp) # recuperando localizacao da variavel lightPos na GPU
        glUniform3f(loc_light_pos, t_x, t_y, t_z) ### posicao da fonte de luz


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