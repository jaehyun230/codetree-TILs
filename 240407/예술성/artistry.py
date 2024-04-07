from collections import deque

n = int(input())

graph = []

for _ in range(n) :
    graph.append(list(map(int, input().split())))


sections = []

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def find(a, b, v) :
    q = deque()
    q.append((a, b))
    v[a][b] = True
    temp = []
    while q :
        x, y = q.popleft()
        temp.append([x, y])
        for i in range(4) :
            mx = x + dx[i]
            my = y + dy[i]
            if 0 <= mx < n and 0 <= my < n and v[mx][my] == False and graph[x][y] == graph[mx][my] :
                v[mx][my] = True
                q.append((mx, my))

    sections.append(temp)

def findsection() :
    global sections
    sections = []
    visited = [[False]*n for _ in range(n)]

    for i in range(n) :
        for j in range(n) :
            if visited[i][j] == False :
                find(i,j, visited)


def calculatesection() :
    global answer

    calculate = 0
    check = [[0]*len(sections) for _ in range(len(sections))]

    for i in range(n) :
        for j in range(n) :

            for a, sec in enumerate(sections) :
                if [i, j] in sec :
                    # i,j 는 a section에
                    # print(a, i, j)
                    for k in range(4) :
                        mx = i + dx[k]
                        my = j + dy[k]
                        if 0 <= mx < n and 0 <= my < n and graph[i][j] != graph[mx][my] :
                            for b, sec2 in enumerate(sections) :
                                if [mx, my] in sec2 :
                                    # print(i, j,  mx, my,  a, b)
                                    check[a][b] +=1

    for i in range(len(sections)) :
        for j in range(len(sections)) :
            if check[i][j] != 0 :

                size = len(sections[i]) + len(sections[j])
                a, b = sections[i][0][0], sections[i][0][1]
                c, d = sections[j][0][0], sections[j][0][1]
                size = size * graph[a][b]
                size = size * graph[c][d]
                size = size * check[i][j]
                calculate += size
    calculate = calculate//2
    answer += calculate

def rotate_maps():
    global graph
    t_maps = [ [0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == n//2 or j == n//2:
                t_maps[n-j-1][i] = graph[i][j]
    d = n//2
    mini_rotate(0,0,d,t_maps)
    mini_rotate(n-d,0,d,t_maps)
    mini_rotate(0,n-d,d,t_maps)
    mini_rotate(n-d,n-d,d,t_maps)

    graph = [ [ t_maps[i][j] for j in range(n)] for i in range(n)]
    return

def mini_rotate(x,y,d,t_maps):

    for i in range(d):
        for j in range(d):
            t_maps[j+x][d-1-i+y] = graph[i+x][j+y]
    return

answer = 0
findsection()
calculatesection()
for _ in range(3) :
    rotate_maps()
    findsection()
    calculatesection()

print(answer)