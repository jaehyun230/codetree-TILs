from collections import deque

# 체스판 크기, 기사 수, 명령어 수
N, M, Q = map(int, input().split())
# 게임판
graph = []
# 기사 정보 저장
knights = []
# 기사 위치 그래프
knights_graph = [[-1] * N for _ in range(N)]
# 기사 생존 여부 체크
knights_alive = [True] * M
# 기사 점수 저장
knights_score = [0] * M
# 이동 방향 - 위 오른 아래 왼
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 기사 판 업데이트
def knights_init() :
    global knights_graph

    knights_graph = [[-1] * N for _ in range(N)]

    for idx, knight in enumerate(knights) :
        # 죽은 기사의경우 판 데이터 업데이트 반영 x
        if knights_alive[idx] == False :
            continue
        cr, cc, ch, cw, ck = knight

        for i in range(cr, cr+ch) :
            for j in range(cc, cc+cw) :
                knights_graph[i][j] = idx

# 왕 움직여라 명령어 수행
def attack(knight_num, move_d) :
    global knights_alive
    global knights_score
    global knights

    q = deque()
    q.append(knight_num)

    temp_damage = [0] * M
    # 이동 한 기사 번호들 기록
    move_sets = set()
    move_sets.add(knight_num)

    check_graph = [[-1]*N for _ in range(N)]

    while q :
        num = q.popleft()
        # 기사 정보 가져오기
        cr, cc, ch, cw, ck = knights[num]

        for i in range(cr, cr+ch) :
            for j in range(cc, cc+cw) :
                # 움직여서 위치할 포인트
                mx = i + dx[move_d]
                my = j + dy[move_d]

                # 이동 하려는 위치가 판 내부이고 벽이 아니어야함
                if 0 <= mx < N and 0 <= my < N and graph[mx][my] != 2 :

                    check_graph[mx][my] = num
                    # 움직이는 위치가 기사가 있고 연쇄작용 큐에 안들어간 기사인 경우
                    if knights_graph[mx][my] != -1 and knights_graph[mx][my] not in move_sets :
                        move_sets.add(knights_graph[mx][my])
                        q.append(knights_graph[mx][my])
                    # 만약 이동되어지는 위치가 함정인 경우 데미지 정보저장 -> 추후 초기 기사는 데미지 0 초기화필요
                    if graph[mx][my] == 1 :
                        temp_damage[num] +=1

                # 이동 불가능 한 경우
                else :
                    return

    # 다 이동할 수 있는 경우 작동
    # 초기 기사는 데미지 받지 않음
    temp_damage[knight_num] = 0
    for kid in move_sets :

        nr, nc, nh, nw, nk = knights[kid]
        # 만약 체력 이상의 데미지를 받은 경우
        if nk <= temp_damage[kid] :
            knights_alive[kid] = False
            continue
        # 체력보다 덜 맞은 경우 점수 흑득
        knights_score[kid] += temp_damage[kid]
        # 함정에 깎인 체력 값도 변경
        nk -= temp_damage[kid]

        # 기사 이동한 정보로 업데이트
        change_r = nr + dx[move_d]
        change_c = nc + dy[move_d]
        # 기사 정보 업데이트
        knights[kid] = [change_r, change_c, nh, nw, nk]


# 체스판 입력 - 0 빈칸 1 함정 2 벽
for _ in range(N) :
    graph.append(list(map(int, input().split())))

# 기사의 위치 좌표 입력
for _ in range(M) :
    r, c, h, w, k = map(int, input().split())
    # 실제 보드는 크기가 작아서 바꿈
    knights.append([r-1, c-1, h, w, k])

# 게임 시작 전 기사 그래프 정보 삽입
knights_init()
# 왕의 명령에 대한 정보
for _ in range(Q) :
    #명령받을 기사 번호 / 이동 방향
    command_id, direction = map(int, input().split())
    # 해당 기사가 살아있으면 수행
    if knights_alive[command_id-1] == True :
        attack(command_id-1, direction)
    knights_init()

answer = 0
for value in range(M) :
    if knights_alive[value] == True :
        answer += knights_score[value]

print(answer)