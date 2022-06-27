#pragma once

#include <array>

class Transform
{
public:
        std::array<float, 3> position;
        std::array<float, 3> rotation;
        std::array<float, 3> scale;
        Transform();

        void setPosition(float x, float y, float z);
        void setRotation(float x, float y, float z);
        void setScale(float x, float y, float z);

        void rotate(float x, float y, float z);
};