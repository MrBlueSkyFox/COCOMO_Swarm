def toint(x, minx, maxx, n):
    x = float(x)
    minx = float(minx)
    maxx = float(maxx)
    x = x - minx
    x = x / (maxx - minx)
    x = int(round(x * 2**n))
    return x

def fromint(x, minx, maxx, n):
    minx = float(minx)
    maxx = float(maxx)
    x = float(x) / 2**n
    x = x * (maxx - minx)
    x = x + minx
    return x

x = -7
minx = -10
maxx = 10
n = 16

x1 = toint(x, minx, maxx, n)
print(bin(x1))
x2 = fromint(x1, minx, maxx, n)
print(x2)