import math

#Calculates the area of a triangle with side lengths a, b, and c.
#PRECONDITION: triangle ABC is a valid triangle.
def triArea(a,b,c):
    s = (a+b+c)/2
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))
    return area
    
#Calculates the sidelength of the radar shape based on the 2 other sides using the Law of Cosines.
def sideLength(r1, r2):
    side_squared = r1**2 + r2**2 - 2*r1*r2*math.cos(2*math.pi/3)
    return math.sqrt(side_squared)

PERFECT_A=1
PERFECT_B=1
PERFECT_C=1
PERFECT_AREA=triArea(sideLength(PERFECT_A,PERFECT_B), sideLength(PERFECT_C,PERFECT_B), sideLength(PERFECT_A,PERFECT_C))