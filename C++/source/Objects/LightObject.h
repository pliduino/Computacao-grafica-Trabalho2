#include <array>
#include "Object.h"

class LightObject : public Object{
    public:
        std::array<float, 3> getColor();
        void setColor(float r, float g, float b);
    
    private:
        std::array<float, 3> color;

};