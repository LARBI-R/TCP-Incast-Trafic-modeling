#example resolution equation second ordre

import math

a = float(input("entrer a"))
b = float(input("entrer b"))
c = float(input("entrer c"))

if a == 0 :
	print("erreur")

Delta = b*b - 4*a*c

if Delta > 0:
	x1 = (-b-math.sqrt(Delta))/(2*a)
	x2 = (-b+math.sqrt(Delta))/(2*a)
	print("x1 = %f x2 = %f" %(x1, x2))
else :
	Delta = -Delta;
	denum = 1/(2*a)
	x1 = (-b/denum)
	x2 = math.sqrt(Delta)
	print("x1 = %f-j%f x2 = %f+j%f" %(x1,x2,x1,x2))


