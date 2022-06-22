from OpenGL.GL import *

class Shader:
    
    def __init__(self):
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

    def get_program(self):
        return self._program