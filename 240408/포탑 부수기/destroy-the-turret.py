import heapq
from collections import deque

graph = []

powerful = []

weaker = []

n, m, K = map(int, input().split())

#최근 공격 시간 따로 관리 heapq 넣을떄 활용
attack_time = [[0]*n for _ in range(n)]

for _ in range(n) :
    graph.append(list(map(int, input().split())))


# 우 하 좌 상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

ddx = [-1, -1, -1, 0, 0, 1, 1, 1]
ddy = [-1, 0, 1, -1, 1, -1, 0, 1]

# 가장 강한 포탑, 약한 포탑 찾기
def in_tower() :
    global weaker
    global powerful
    #초기화 후 집어넣기
    weaker = []
    powerful = []

    for i in range(n) :
        for j in range(n) :
            if graph[i][j] > 0 :
                # 가장 약한 포탑 집어넣기
                heapq.heappush(weaker, [graph[i][j], attack_time[i][j]*-1, (i+j)*-1, (j)*-1, i*-1])
                # 가장 강한 포탑 집어넣기
                heapq.heappush(powerful, [graph[i][j]*-1, attack_time[i][j], (i+j), j, i])


def raserattack(x, y, x2, y2) :
    q = deque()
    q.append([x, y, []])
    visited = [[False]*n for _ in range(n)]
    visited[x][y] = True

    while q :
        nx, ny, path = q.popleft()
        if nx == x2 and ny == y2 :
            return path
        for i in range(4) :
            mx = nx + dx[i]
            my = ny + dy[i]

            if mx < 0 :
                mx = n-1
            if my < 0 :
                my = n-1
            if mx >= n :
                mx = 0
            if my >= n :
                my = 0

            if graph[mx][my] != 0 and visited[mx][my] == False :
                visited[mx][my] = True
                q.append([mx, my, path+[[mx, my]]])

    return []

def cannonattack(x, y, x2, y2, power) :

    temp = [[x2, y2], [x, y]]
    for i in range(8) :
        mx = x2 + ddx[i]
        my = y2 + ddy[i]

        if mx < 0:
            mx = n - 1
        if my < 0:
            my = n - 1
        if mx >= n:
            mx = 0
        if my >= n:
            my = 0

        temp.append([mx, my])

        graph[mx][my] -= power//2
        if graph[mx][my] < 0 :
            graph[mx][my] = 0

    graph[x2][y2] = graph[x2][y2] - power
    if graph[x2][y2] < 0 :
        graph[x2][y2] = 0

    for i in range(n) :
        for j in range(n) :
            if graph[i][j] > 0 and [i,j] not in temp :
                graph[i][j] +=1

def update(x, y, power) :
    graph[x][y] = power
    attack_time[x][y] = Time

def calculate_laser_path(path, power) :

    x2, y2 = path[-1]
    graph[x2][y2] += power//2

    for x,y in path :
        graph[x][y] -= power//2
        if graph[x][y] < 0 :
            graph[x][y] = 0

    x2, y2 = path[-1]
    graph[x2][y2] -= power
    if graph[x2][y2] < 0 :
        graph[x2][y2] = 0


def play() :

    #공격자 선정
    attacker = heapq.heappop(weaker)

    power, _, _, y, x = attacker
    y = y*-1
    x = x*-1
    # 공격자 파워 얻음
    power = power+(n+m)

    #가장 강한 포탑 찾기
    target = heapq.heappop(powerful)
    target_x, target_y = target[4], target[3]

    result = raserattack(x, y, target_x, target_y)
    if len(result) == 0 :
        cannonattack(x, y, target_x, target_y, power)
    else :
        calculate_laser_path(result, power)
        for i in range(n) :
            for j in range(n) :
                if graph[i][j] > 0 and [i,j] not in result :
                    graph[i][j] +=1
                    if i == x and j == y :
                        graph[i][j] -=1

    #공격 안받은 포탑들 공 +1 시켜야함
    update(x, y, power)


Time = 1
while Time <= K :
    in_tower()
    if len(weaker) == 1 :
        break
    play()
    Time +=1


# for 문 돌려야할 듯
max_val = 0
for i in range(n) :
    for j in range(n) :
        if graph[i][j] > max_val :
            max_val = graph[i][j]

print(max_val)