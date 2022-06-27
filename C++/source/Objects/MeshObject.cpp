#include <fstream>
#include <string>
#include <sstream>
#include "MeshObject.hpp"

std::vector<std::string> split(std::string s, std::string del = " ")
{
    std::stringstream ss(s);
    int start = 0;
    int end = s.find(del);
    std::vector<std::string> splittedString;

    while (end != -1)
    {
        splittedString.push_back(s.substr(start, end - start));
        start = end + del.size();
        end = s.find(del, start);
    }

    return splittedString;
}

MeshObject::MeshObject()
{
    ns = 16;
    ka = 0.5;
    kd = 0.5;
    ks = 0.5;
}

void MeshObject::loadMeshFile(std::string filename)
{
    std::vector<float> vertices, normals, texture_coords;
    std::vector<std::array<std::vector<int>, 3>> faces;
    std::string material = "";
    std::vector<std::string> materials;

    std::ifstream objFile(filename, std::ifstream::in);
    for (std::string line; std::getline(objFile, line);)
    {
        // Skipping comments
        if (line[0] == '#')
            continue;

        // Breaking line into words
        std::vector<std::string> values = split(line);

        // Reading vertices
        if (values[0] == "v")
        {
            for (int i = 1; i < 4; i++)
                vertices.push_back(std::stof(values[i]));
        }

        // Reading normals
        else if (values[0] == "vn")
        {
            for (int i = 1; i < 4; i++)
                normals.push_back(std::stof(values[i]));
        }

        // Reading texture coordinates
        else if (values[0] == "vt")
        {
            for (int i = 1; i < 3; i++)
                texture_coords.push_back(std::stof(values[i]));
        }

        // Reading material
        else if (values[0] == "usemtl" || values[0] == "usemat")
        {
            for (int i = 1; i < 3; i++)
                material = values[1];
        }

        // Reading faces
        else if (values[0] == "f")
        {
            std::vector<int> face, face_texture, face_normals;
            for (auto v : values)
            {
                std::vector<std::string> w = split(v, "/");
                face.push_back(std::stoi(w[0]));

                // Checks for existing face_texture
                if (w[1].empty())
                    face_texture.push_back(0);
                else
                    face_texture.push_back(stoi(w[1]));

                face_normals.push_back(std::stoi(w[2]));
            }
            faces.push_back(std::array{face, face_texture, face_normals});
            materials.push_back(material);
        }
    }
}

void MeshObject::setTexture(int texture_id)
{
    textureId = texture_id;
}

void MeshObject::setProperties(float nns, float nka, float nkd, float nks)
{
    ns = nns;
    ka = nka;
    kd = nkd;
    ks = nks;
}