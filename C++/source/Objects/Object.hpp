#pragma once

#include <iostream>
#include "Transform.cpp"

class Object
{
public:
    Transform transform;

    Object();

    /**
     * @brief Called every frame
     * 
     * @param delta Time passed between tick calls
     */
    virtual void tick(float delta);
};