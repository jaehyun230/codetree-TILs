from collections import deque

# 위 왼 오 아  우선 순위로 탐색
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

n, m = map(int, input().split())

graph = []

#이동 가능한 사람들 - people 에서 나와 들어갈 부분들
move_people = []

# m번 사람들이 각각 가지고있는 목적지가 들어갈 예정
people = deque()

for _ in range(n) :
    graph.append(list(map(int, input().split())))

for _ in range(m) :
    # 해당 사람이 가고자 하는 목적지
    x ,y = map(int ,input().split())

    people.append([x-1, y-1])


def find_start_base_camp(x, y) :
    q = deque()

    max_d = 31

    q.append([x, y, 0])

    visited = [[False]*n for _ in range(n)]
    visited[x][y] = True

    start = [-1, -1]

    while q :
        #현재 위치
        nx, ny, nd = q.popleft()

        for i in range(4) :
            mx = nx + dx[i]
            my = ny + dy[i]

            # graph[mx][my] -> -1 이면 앞으로 사용못하게되는경로인 부분인것
            if 0 <= mx < n and 0 <= my < n and graph[mx][my] != -1 and visited[mx][my] == False :
                visited[mx][my] = True
                # 해당위치가 베이스 캠프 인 경우
                if graph[mx][my] == 1 :
                    #처음 찾은 최단경로
                    if max_d == 31 :
                        start = [mx, my]
                        max_d = nd
                    else :
                        if nd > max_d :
                            continue
                        # 행이 작다면 변경
                        if start[0] > mx :
                            start = [mx, my]
                        elif start[0] == mx and start[1] > my :
                            start = [mx, my]
                # 찾은 최단경로보다 크면 더 이상 추가 탐색 x
                if nd < max_d :
                    q.append([mx, my, nd+1])

    return start[0], start[1]

def find_one_step(nx, ny, tx, ty) :

    q = deque()

    visited = [[False]*n for _ in range(n)]

    visited[nx][ny] = True

    for i in range(4) :
        mx = nx + dx[i]
        my = ny + dy[i]
        if 0 <= mx < n and 0 <= my < n and graph[mx][my] != -1 and visited[mx][my] == False :
            visited[mx][my] = True

            if mx == tx and my == ty :
                return i
            # 3번째는 시작한 방향
            q.append([mx, my, i])

    while q :
        x, y, d = q.popleft()

        for i in range(4) :
            mx = x + dx[i]
            my = y + dy[i]

            if 0 <= mx < n and 0 <= my < n and graph[mx][my] != -1 and visited[mx][my] == False :
                visited[mx][my] = True

                if mx == tx and my == ty :
                    return d
                q.append([mx, my, d])


def move_people_move() :
    global move_people

    for i in range(len(move_people)) :
        nx, ny, tx, ty = move_people[i]
        # 이미 도착한 사람은 패스
        if nx == tx and ny == ty :
            continue

        dir = find_one_step(nx, ny, tx, ty)
        nx = nx + dx[dir]
        ny = ny + dy[dir]
        move_people[i] = [nx, ny, tx, ty]



# 사람들 도착했나 확인
def check_people_final() :

    for i in range(len(move_people)) :
        nx, ny, tx, ty = move_people[i]
        if nx == tx and ny == ty :
            graph[nx][ny] = -1

def check_game_end() :
    if not move_people :
        return False

    for i in range(len(move_people)) :
        nx, ny, tx, ty = move_people[i]
        if nx != tx or ny != ty :
            return False

    return True


time = 1
# 아직 출발 안한 사람이나 or 출발하고 도착지점 못간 사람 조건
while True :

    # print("now time ", time)
    # 격자에 있는사람 (move_people) 모두 자신의 목표점에 1칸 이동
    move_people_move()
    # 모든 사람들이 이동 한 후 편의점 도착한 사람들 위치는 앞으로 이동 불가로 변경
    check_people_final()

    # time m 이하 사람 배출
    if people :
        x, y = people.popleft()
        # 자신의 목적지에서 가장 가까운 베이스 캠프 탐색
        sx, sy = find_start_base_camp(x, y)
        # print("find start " , sx, sy)
        # 격자판 안에 시작 베이스 캠프 위치에 사람 집어 넣기
        move_people.append([sx, sy, x, y])
        # 집어 넣은 베이스 캠프 위치 앞으로 사용 불가
        graph[sx][sy] = -1


        # 모든 사람이 출발 하였고 도착지점에 완료 한 경우
    if check_game_end() == True :
        break

    time +=1

print(time)