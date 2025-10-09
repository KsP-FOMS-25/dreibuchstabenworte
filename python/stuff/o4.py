x = ["abc","123","def","456"]
y = ["abc","123","def","456"]
x is y, x == y
z = x 
x is y, y is z, y is z, x is z
x is not y, x is not z, x is not z
del x[1]
print(x, y, z)