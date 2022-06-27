#include "LightObject.hpp"

std::array<float, 3> LightObject::getColor()
{
        return color;
}

void LightObject::setColor(float r, float g, float b)
{
        color = {r, g, b};
}