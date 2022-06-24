vec3 ambientLightColor = vec3(1.0, 1.0, 1.0);

const int LIGHTSLOTS = 5;

uniform vec3 lightColor[LIGHTSLOTS];
uniform vec3 lightPos[LIGHTSLOTS];


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
    vec3 ambient = ka * ambientLightColor;             
    vec3 specular = vec3(0, 0, 0);
    vec3 diffuse = vec3(0, 0, 0);

    for (int i = 0; i < LIGHTSLOTS; i++){
        // Diffuse
        vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
        vec3 lightDir = normalize(lightPos[i] - out_fragPos); // direcao da luz
        float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
        diffuse += kd * diff * lightColor[i]; // iluminacao difusa

        // Specular
        vec3 viewDir = normalize(viewPos - out_fragPos);
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
        specular += ks * spec * lightColor[i];           

    }
    
    // aplicando o modelo de iluminacao
    vec4 texture = texture2D(samplerTexture, out_texture);
    vec4 result = vec4((ambient + diffuse + specular), 1.0) * texture; // aplica iluminacao
    gl_FragColor = result;

}