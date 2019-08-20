from opytic import *

#ðefine the lenses surfaces
s1_lens1 = aspheric_surface(8.818197, -0.9991715, 8.682167*10**(-5), 6.3760123*10**(-8), 2.4073084*10**(-9),-1.7189021*10**(-11))
s2_lens1 = aspheric_surface(-69.99948)

#build the optical objects
lens1 = lens(s1_lens1,s2_lens1,25.4/2,1.2,16.0,7.3,1.52,0)
interface1 = interface(1.5,1,12)
mirror1 = mirror(flat_surface(-pi/4),-20)

#build the simulation beams
beams = [beam(-20+h,15,-pi/2) for h in np.arange(-5,5,1)]

#for each beams process its path
for ray in beams:
    ray.go_through(mirror1)
    ray.go_through(lens1)
    ray.go_through(interface1)
    #prints the rays
    ray.draw(40)

#prints the optical objects
interface1.draw(20)
lens1.draw()
mirror1.draw(-10,10)
show()
