N, M, K = map(int, input().split())

# 그래프
graph = []

# 손님
guest = []

# 탈출 손님 체크
guest_end = [False] * M

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 시계방향 부분 90도 부분 회전 내구도 1 감소
def rotate_90(sx, sy, length):

    global exit
    global guest

    temp = [[0]*N for _ in range(N)]

    guest_data = []
    exit_data = []

    # 정사각형을 시계방향으로 90도 회전
    for x in range(sx, sx + length):
        for y in range(sy, sy + length):

            # 1단계 : (0,0)으로 옮겨주는 변환을 진행함
            ox, oy = x - sx, y - sy
            # 2단계 : 90도 회전했을때의 좌표를 구함
            rx, ry = oy, length - ox - 1
            # 3단계 : 다시 (sy,sx)를 더해줌
            temp[sx + rx][sy + ry] = graph[x][y]

            # 출구 위치 변경 임시저장
            if x == exit[0] and y == exit[1] :
                exit_data.append([sx+rx, sy+ry])

            # 손님도 위치 변경되면 변경 임시저장 ( 다돌고 변경해야함)
            for g in range(M) :
                if guest_end[g] == True :
                    continue
                gx, gy = guest[g]
                if x == gx and y == gy :
                    guest_data.append([sx+rx, sy+ry, g])


    # 출구 위치 업데이트
    for data in exit_data :
        ea, eb = data
        exit = [ea, eb]

    # 게스트 데이터 위치 업데이트
    for data in guest_data :
        a, b, c = data
        guest[c] = [a, b]

    for i in range(sx, sx+length) :
        for j in range(sy, sy+length) :
            #실제는 회전하면서 벽 내구도 감소
            if temp[i][j] >= 1 :
                temp[i][j] -=1
            graph[i][j] = temp[i][j]


for _ in range(N) :
    graph.append(list(map(int, input().split())))

for idx in range(M) :
    x, y = map(int, input().split())
    guest.append([x-1, y-1])

ex, ey = map(int, input().split())

# 출구 위치
exit = [ex-1, ey-1]

count = 0
total_walk = 0

def do_walk(x, y) :

    distance = abs(x-exit[0]) + abs(y-exit[1])

    for i in range(4) :
        mx = x + dx[i]
        my = y + dy[i]

        if 0 <= mx < N and 0 <= my < N and graph[mx][my] == 0 :
            # 더 짧은 최단거리 존재하면 해당 걸음으로 이동
            if distance > abs(mx-exit[0]) + abs(my-exit[1]) :
                return [mx, my]

    return [x, y]

def guest_walk() :
    global guest
    global total_walk
    for idx in range(M) :
        if guest_end[idx] == True :
            continue
        x, y = guest[idx]
        nx, ny = do_walk(x, y)

        # 위치가 변했으면 1걸음 이동한 것
        if x!= nx or y != ny :
            total_walk +=1
        # 만약 출구에 도달했다면 해당 손님은 도착
        if nx == exit[0] and ny == exit[1] :
            guest_end[idx] = True
        # 손님 좌표 업데이트
        guest[idx] = [nx, ny]

def find_rotation() :

    # return 할 정사각형 시작 위치와 길이
    sx, sy, sqare_length = -1, -1, 200
    # 출구 위치
    ex, ey = exit[0], exit[1]

    for idx in range(M) :
        # 이미 도착한 손님은 제외
        if guest_end[idx] == True :
            continue
        gx, gy = guest[idx]

        # 손님과 출구 간의 가장 작은 사각형 사이즈
        square_size = max(abs(gx-ex), abs(gy-ey))

        sqare_length = min(square_size, sqare_length)

    for i in range(N-sqare_length) :
        for j in range(N-sqare_length) :
            if i <= ex <= i + sqare_length and j <= ey <= j + sqare_length :

                for idx in range(M) :
                    if guest_end[idx] == False :
                        mx, my = guest[idx]

                        if i <= mx <= i + sqare_length and j <= my <= j + sqare_length :
                            return [i, j, sqare_length+1]


    return [sx, sy, sqare_length]

count = 1
while count <= K :

    #손님들 걸음 활동
    guest_walk()
    # 가장 작은 정사각형 찾기 - 한명이상의 참가자와 출구포함된, 크기가 가장 작은것 우선순위, 다음 행이 작은게, 다음 열이 작은게 우선 순위
    sx, sy, sqare_length = find_rotation()
    # print(exit,  sx, sy, sqare_length)
    # 로테이션 위치 못찾은경우 -> 손님들이 이미 다 출구에 도착한 경우
    if sqare_length == 200 :
        break
    rotate_90(sx, sy, sqare_length)
    count +=1


print(total_walk)
print(exit[0]+1, exit[1]+1)