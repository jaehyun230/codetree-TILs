# 상 하 로 우선순위로 이동
dx = [-1, 1, 0 ,0]
dy = [0, 0, 1, -1]

# 게임판크기, m명참가자 수, k초동안 반복
N, M, K = map(int, input().split())

graph = []

guest = []
# 탈출한 손님 기록할 부분
guest_end = [False] * M

for _ in range(N) :
    graph.append(list(map(int, input().split())))

for idx in range(M) :
    g_x, g_y = map(int, input().split())
    # 프로그램에선 0,0 부터 시작할 것 해당위치 idx 손님이 있음
    guest.append([g_x-1, g_y-1, idx])

e_x, e_y = map(int, input().split())
exit = [e_x-1, e_y-1]

def move(gx, gy, idx) :
    global answer
    # 현재 출구와의 거리
    now_dist = abs(gx-exit[0]) + abs(gy-exit[1])

    result_x, result_y = gx, gy


    for i in range(4) :
        mx = gx + dx[i]
        my = gy + dy[i]
        # 공간 범위내고 해당 위치가 벽이 없어야함
        if 0 <= mx < N and 0 <= my < N and graph[mx][my] == 0 :
            # 이동 하였을 경우 거리
            new_dist = abs(mx-exit[0]) + abs(my-exit[1])
            # 우선순위 순서대로 움직임
            if new_dist < now_dist :
                result_x, result_y = mx, my
                now_dist = new_dist

    # 해당 게스트 위치 업데이트
    guest[idx] = [result_x, result_y, idx]
    # 해당 게스트가 탈출 한위치라면
    if result_x == exit[0] and result_y == exit[1] :
        guest_end[idx] = True

    # 위치가 하나라도 변했으면 움직인거기 때문에
    if result_x != gx or result_y != gy :
        answer +=1



def guest_move() :
    for g in guest :
        # 게스트의 위치, 번호
        gx, gy, idx = g
        # 이미 도착한 참가자는 패스
        if guest_end[idx] == True :
            continue
        move(gx, gy, idx)

def find_rec_size() :
    rec_size = 1000

    for g in guest :
        gx, gy, idx = g
        if guest_end[idx] == True :
            continue

        new_size = max(abs(gx-exit[0]), abs(gy-exit[1]))
        # 더 작은 사각형을 찾는 다면
        if new_size < rec_size :
            rec_size = new_size

    # 실제로는 거리는 2지만 사각형을 그려보면 길이가 3임
    return rec_size + 1

# 회전을 시작할 위치 찾기
def find_rotate_pos(size) :

    rx, ry = -1, -1

    for i in range(N-size+1) :
        for j in range(N-size+1) :

            # 사각형 안에 출구가 있으면
            if i <= exit[0] < i +size and j <= exit[1] < j + size :

                for g in guest :
                    gx, gy, idx = g
                    # 끝난 guest 는 패스
                    if guest_end[idx] == True :
                        continue

                    if i <= gx < i +size and j <= gy < j + size :
                        return [i, j]


# 90도 부분회전 - 시작위치 / 사이즈
def rotate_90(rx, ry, size) :
    global exit

    temp = [[0]*N for _ in range(N)]

    temp_exit = []
    temp_guest = []


    for i in range(rx, rx+size) :
        for j in range(ry, ry+size) :
            ox, oy = i-rx, j-ry
            x, y = oy, size-ox-1
            temp[rx+x][ry+y] = graph[i][j]

            # 회전하는 위치 손님있으면 해당 손님도 위치 업데이트 해줘야함
            for g in guest :
                gx, gy, idx = g
                # 끝난 guest 는 패스
                if guest_end[idx] == True:
                    continue

                if gx == i and gy == j :
                    temp_guest.append([rx+x, ry+y, idx])

            if i == exit[0] and j == exit[1] :
                temp_exit.append([rx+x, ry+y])

    for i in range(rx, rx+size) :
        for j in range(ry, ry+size) :
            if temp[i][j] > 0 :
                temp[i][j] -=1
            graph[i][j] = temp[i][j]

    # 회전에 의한
    # 출구 업데이트
    for x, y in temp_exit :
        exit = [x, y]
    # 게스트 위치 업데이트

    for nx, ny, nidx in temp_guest :
        guest[nidx] = [nx, ny, nidx]


time = 0
answer = 0
while time < K :
    # 손님들 움직임
    guest_move()
    # 가장 작은 정사각형 찾기
    rec_size = find_rec_size()
    # 손님이 다 탈출한 경우
    if rec_size == 1001 :
        break
    # 회전 시작할 위치
    rx, ry = find_rotate_pos(rec_size)
    rotate_90(rx, ry, rec_size)
    time +=1

print(answer)
print(exit[0]+1, exit[1]+1)