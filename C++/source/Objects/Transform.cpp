
#include "Transform.h"



Transform::Transform(){
        position = {0, 0, 0};
        rotation = {0, 0, 0};
        scale = {1, 1, 1};
    }

void Transform::setPosition(float x, float y, float z){
    position = {x, y, z};
}

void Transform::setRotation(float x, float y, float z){
    rotation = {x, y, z};
}

void Transform::setScale(float x, float y, float z){
    scale = {x, y, z};
}

void Transform::rotate(float x, float y, float z){
    rotation = {rotation[0] + x, rotation[1] + y, rotation[2] + z};
}

