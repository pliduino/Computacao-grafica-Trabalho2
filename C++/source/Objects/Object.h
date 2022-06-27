#pragma once

#include <iostream>
#include "Transform.cpp"

class Object{
    public:
        Transform transform;
        
        Object();
        virtual void tick(float delta);
};