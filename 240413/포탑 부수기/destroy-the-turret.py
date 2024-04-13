import heapq
from collections import deque

N, M, K = map(int, input().split())
# 게임판
graph =[]
# 포탑 정보
tower = []
# 강한 정보
power_tower = []
# 약한 정보
weak_tower = []

# 우 하 좌 상
dx = [0, 1, 0, -1, -1, -1, 1, 1]
dy = [1, 0, -1, 0, -1, 1, -1, 1]

for _ in range(N) :
    graph.append(list(map(int, input().split())))

# 타워 정보 넣는 순간
def init_tower() :
    global tower

    tower = []

    number = 0
    for i in range(N):
        for j in range(N):
            if graph[i][j] != 0:
                tower.append([graph[i][j], 0, i, j, number])
                number +=1


time = 0

# 공격자와 맞을자 선정
def find_attacker_defenser() :

    te1 = tower
    power_tower = []
    weak_tower = []

    if len(tower) == 0 :
        return [-1, -1]

    for k in range(len(tower)) :
        p, attack_count, x_pos, y_pos, k = tower[k]

        # 공격자 우선순위 - 공격력 낮고, 제일최근 공격, 행열 합 높은, 열 높은, 친구 - 뒤에는 해당 타워 넘버 추가함 그냥
        heapq.heappush(weak_tower, [p, attack_count*-1, (x_pos+y_pos)*-1, y_pos *-1, k])

        heapq.heappush(power_tower, [p*-1, attack_count, (x_pos+y_pos), y_pos, k])


    _ , _, _, _, num1 = heapq.heappop(weak_tower)
    _, _, _, _, num2 = heapq.heappop(power_tower)


    return [num1, num2]

def find_attack_route(num1, num2) :

    p1, attack_count, x1, y1, idx1 = tower[num1]

    p2, attack_count2, x2, y2, idx2 = tower[num2]

    q = deque()

    visited = [[False] * N for _ in range(N)]

    q.append([x1, y1, [[x1, y1]]])
    visited[x1][y1] = True

    while q :

        x, y, path = q.popleft()

        for i in range(4) :
            mx = x + dx[i]
            my = y + dy[i]

            # 넘어간 경우
            if mx >= N :
                mx = 0
            elif my >= N :
                my = 0
            elif mx < 0 :
                mx = N -1
            elif my < 0 :
                my = N -1

            if 0 <= mx < N and 0 <= my < N and graph[mx][my] != 0 and visited[mx][my] == False :
                visited[mx][my] = True
                if mx == x2 and my == y2 :
                    return path +[[mx, my]]
                q.append([mx, my, path +[[mx, my]]])


    return []

def attack_raser(paths, idx) :

    global tower

    p1, attack_count, x1, y1, idx = tower[idx]

    p1 += N+M
    attack_count +=1

    tower[idx] = [p1, attack_count, x1, y1, idx]
    temp_tower = []


    for t in tower :
        p, ac, x, y, num = t
        if [x,y] == paths[0] :

            temp_tower.append(t)

            continue

        elif [x,y] == paths[-1] :
            p = p-p1

            if p <= 0 :
                continue
            else :
                temp_tower.append([p, ac, x, y, num])

        elif [x,y] in paths :
            p = p - p1//2
            if p <= 0:
                continue
            else:
                temp_tower.append([p, ac, x, y, num])

        # 게임과 상관없는 타워들은 공 +=1
        else :
            temp_tower.append([p+1, ac, x, y, num])

    tower = temp_tower

def attack_cannon(num1, num2) :

    global tower

    p1, attack_count, x1, y1, idx1 = tower[num1]
    p2, attack_count2, x2, y2, idx2 = tower[num2]

    temp_tower = []

    p1 = p1 + N + M
    attack_count +=1

    temp_tower.append([p1, attack_count, x1, y1, idx1])

    p2 = p2-p1
    if p2 > 0 :
        temp_tower.append([p2, attack_count2, x2, y2, idx2])

    for i in range(8) :
        mx = x2 + dx[i]
        my = y2 + dy[i]

        if mx < 0 :
            mx = N -1
        elif mx >= N :
            mx = 0

        if my < 0 :
            my = N -1
        elif my >= N :
            my = 0

        if mx == x1 and my == y1 :
            continue
        elif mx == x2 and my == y2 :
            continue

        for t in tower:
            np, nac, nx, ny, nnum = t

            if nx == mx and ny == my :
                np = np - p1 // 2
                if np <= 0:
                    continue
                else:
                    temp_tower.append([np, nac, nx, ny, nnum])

    tower = temp_tower


def update_tower() :
    global tower

    temp = []
    for num, t in enumerate(tower) :
        p, ac, x, y, _ = t
        temp.append([p, ac, x, y, num])

    tower = temp
def update_graph() :

    global graph

    graph = [[0]*N for _ in range(N)]


    for t in tower :
        p, ac, x, y, num = t
        graph[x][y] = p


init_tower()
while time < K :
    attack_idx, defense_idx = find_attacker_defenser()
    # 살아있는 포탑이 없거나 하나만 남은 경우
    if attack_idx == defense_idx :
        break

    path = find_attack_route(attack_idx, defense_idx)

    if len(path) == 0 :
        attack_cannon(attack_idx, defense_idx)
    else :
        attack_raser(path, attack_idx)
    update_tower()
    update_graph()
    time +=1

answer = 0
for i in range(N) :
    for j in range(N) :
        answer = max(answer, graph[i][j])

print(answer)