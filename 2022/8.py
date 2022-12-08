
lines = [line.strip() for line in open("input-8.txt")]
#lines = [line.strip() for line in open("input-8-test.txt")]
matrix = [list(map(int, list(line))) for line in lines]

s = len(lines)
visible = set() # (x,y)

for y in range(s):
    h = -1
    for x in range(s):
        if matrix[x][y] > h:
            h = matrix[x][y]
            visible.add( (x,y) )
    h = -1
    for x in range(s - 1, -1, -1):
        if matrix[x][y] > h:
            h = matrix[x][y]
            visible.add( (x,y) )
for x in range(s):
    h = -1
    for y in range(s):
        if matrix[x][y] > h:
            h = matrix[x][y]
            visible.add( (x,y) )
    h = -1
    for y in range(s - 1, -1, -1):
        if matrix[x][y] > h:
            h = matrix[x][y]
            visible.add( (x,y) )

#print(visible)
print(len(visible))

h = 0
for y in range(s):
    for x in range(s):
        ss = 1
        for d in [(0,1),(0,-1),(1,0),(-1,0)]:
            q = 0
            xx = x + d[0]
            yy = y + d[1]
            while xx >= 0 and yy >= 0 and xx < s and yy < s:
                q += 1
                if matrix[xx][yy] >= matrix[x][y]:
                    break
                xx += d[0]
                yy += d[1]
            ss *= q
        if ss > h:
            h = ss
            print(x,y,ss)

print(h)

