from collections import deque

n, m, c = map(int, input().split())

graph = []

dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

for _ in range(n) :
    graph.append(list(map(int, input().split())))

# n 번째 사람의 목적지 정보 저장
people = []

peoplegraph = [[-1] * n for _ in range(n)]

a, b = map(int, input().split())
# 자율 주행차 시작 위치
carpos = [a-1, b-1]

for idx in range(m) :
    #손님 좌표 / 목표 좌표
    sx, sy, tx, ty = map(int, input().split())
    peoplegraph[sx-1][sy-1] = idx
    people.append([tx-1, ty-1])

# 태울 손님 찾기
def find_guest() :
    q = deque()
    a, b = carpos[0], carpos[1]
    q.append([a, b, 0])

    visited = [[False] *n for _ in range(n)]
    visited[a][b] = True

    result = [-1, -1, 401]

    while q:
        x, y, d = q.popleft()
        # 지금 위치에 태울 사람 있으면
        if peoplegraph[x][y] != -1 :
            if result[2] > d :
                result = [x, y, d]
            elif result[2] == d :
                if result[0] > x :
                    result = [x, y, d]
            elif result[2] == d and result[0] == x :
                if result[1] > y :
                    result = [x, y, d]

            continue

        for i in range(4) :
            mx = x + dx[i]
            my = y + dy[i]

            if 0 <= mx < n and 0 <= my < n and visited[mx][my] == False and graph[mx][my] == 0 :
                visited[mx][my] = True
                q.append([mx ,my, d+1])


    # 태울 손님 없음
    return result

def go_target(idx) :

    target_x, target_y = people[idx]

    q = deque()
    a, b = carpos[0], carpos[1]
    q.append([a, b, 0])

    visited = [[False] * n for _ in range(n)]
    visited[a][b] = True
    while q:
        x, y, d = q.popleft()

        if x == target_x and y == target_y:
            return [x, y, d]

        for i in range(4):
            mx = x + dx[i]
            my = y + dy[i]

            if 0 <= mx < n and 0 <= my < n and visited[mx][my] == False and graph[mx][my] == 0:
                visited[mx][my] = True
                q.append([mx, my, d + 1])

    # 목적지 갈 수 없음
    return [-1, -1, -1]


while c >= 0 :
    pos_data = find_guest()
    # 태울 손님 없는 경우 끝
    if pos_data[0] == -1 :
        break
    # 태우러갈 배터리 없는 경우
    if c < pos_data[2] :
        c = -1
        break
    c -= pos_data[2]

    # 손님 타겟 목적지 번호
    target_idx = peoplegraph[pos_data[0]][pos_data[1]]
    # 태운 손님 체크
    peoplegraph[pos_data[0]][pos_data[1]] = -1
    # 현재 차 위치 업데이트
    carpos = [pos_data[0], pos_data[1]]
    # 해당 타겟으로 이동
    nx, ny, need_energe = go_target(target_idx)
    if c < need_energe :
        c = -1
        break
    c = c + need_energe

    carpos = [nx, ny]

for i in range(n) :
    for j in range(n) :
        if peoplegraph[i][j] != -1 :
            c = -1
print(c)