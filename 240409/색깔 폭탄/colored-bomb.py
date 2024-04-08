from collections import deque
import copy

n, m = map(int, input().split())
graph = []

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for _ in range(n) :
    graph.append(list(map(int, input().split())))

# 반시계 90도 회전
def rotation_reverse_90() :
    global graph

    temp = [[0]*n for _ in range(n)]

    for i in range(n) :
        for j in range(n) :
            temp[n-1-j][i] = graph[i][j]

    graph = temp

def find(a, b, visit) :
    q = deque()
    value = graph[a][b]
    q.append([a, b])
    visit[a][b] = True

    path = [[a, b]]
    # 빨간 폭탄 위치 임시체크용
    red = []
    while q :
        x, y = q.popleft()
        for i in range(4) :
            mx = x + dx[i]
            my = y + dy[i]
            if 0 <= mx < n and 0 <= my < n :
                if graph[mx][my] == value and visit[mx][my] == False :
                    visit[mx][my] = True
                    q.append([mx, my])
                    path.append([mx, my])
                elif graph[mx][my] == 0 :
                    if [mx, my] not in red :
                        red.append([mx, my])
                        q.append([mx, my])


    return path, red

# 폭탄 터트리기
def letsboom(boom, red) :
    global answer

    answer += (len(boom)+len(red))**2

    for x, y in boom :
        #터지고 빈공간 -2
        graph[x][y] = -2

    for x, y in red :
        graph[x][y] = -2


#기준점 찾기
def findpoint(data, data2) :
    pos = [-1, 50]

    for x, y in data :
        if x > pos[0] :
            pos[0], pos[1] = x, y
        elif x == pos[0] and y < pos[1] :
            pos[0], pos[1] = x, y

    for x, y in data2 :
        if x > pos[0] :
            pos[0], pos[1] = x, y
        elif x == pos[0] and y < pos[1] :
            pos[0], pos[1] = x, y

    return pos

def findbomb() :
    # 행 높고 열 낮은 우선순위
    visited = [[False]*n for _ in range(n)]

    boom = []
    red_boom = []
    pos = [-1, 50]

    for i in range(n-1, -1, -1) :
        for j in range(n) :
            if graph[i][j] >= 1 :
                path, red = find(i, j, visited)
                if len(path) + len(red) > len(boom) + len(red_boom) :
                    boom = path
                    red_boom = red
                    pos = findpoint(path, red)
                elif len(path) + len(red) == len(boom) + len(red_boom) and len(red) < len(red_boom) :
                    boom = path
                    red_boom = red
                    pos = findpoint(path, red)
                elif len(path) + len(red) == len(boom) + len(red_boom) and len(red) == len(red_boom) :
                    pos2 = findpoint(path, red)
                    if pos[0] < pos2[0] :
                        pos = pos2
                        boom = path
                        red_boom = red
                    elif pos[0] == pos2[0] and pos[1] > pos2[1] :
                        pos = pos2
                        boom = path
                        red_boom = red


    if len(boom) + len(red_boom) >= 2 :
        letsboom(boom, red_boom)
        return True
    # 터트릴 것 못찾음
    return False

def gravity() :
    global graph
    temp = copy.deepcopy(graph)

    for j in range(n) :
        for i in range(n-1, 0, -1) :
            if temp[i][j] == -2 and temp[i-1][j] != -1 :
                temp[i][j], temp[i-1][j] = temp[i-1][j], temp[i][j]

    if temp != graph :
        graph = temp
        gravity()



answer = 0
while True :
    # 폭탄 터트릴께 있으면 터트리고 점수 얻음
    if findbomb() == False :
        break
    # 터트렸으니 중력
    gravity()
    # 반시계 90도 회전
    rotation_reverse_90()
    # 다시 중력
    gravity()

print(answer)