#include <vector>

#include "Object.hpp"

class MeshObject : public Object
{
public:
    unsigned short textureId;
    unsigned verticesIndex;
    unsigned nVertices;

    MeshObject();

    // Loads a Wavefront OBJ
    void loadMeshFile(std::string filename);

    void setTexture(int texture_id);

    // Set Specular Exponent, Ambient Reflection, Diffuse, Specular
    void setProperties(float nns, float nka, float nkd, float nks);

protected:
    float ns, ka, kd, ks; // Specular Exponent, Ambient Reflection, Diffuse, Specular
};