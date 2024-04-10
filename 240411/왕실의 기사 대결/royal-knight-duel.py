L, N, Q = map(int, input().split())

graph = []

knights = []
# 기사 살아있나 확인
alive_knights = [True] * N

knights_score = [0] * N

# -1 이 빈칸 그다음부턴 idx로 기사 번호
knights_graph = [[-1]*L for _ in range(L)]

# 위 오 아 왼 (명령 방향)
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

move_sets = set()

# 나이트 그래프에 기사들 있는지 체크 그림 그리기
def knights_init() :
    global knights_graph

    knights_graph = [[-1] * L for _ in range(L)]

    for knight in knights :
        x, y, h, w, k, idx = knight

        # 죽은 기사 경우 패스
        if alive_knights[idx] == False :
            continue

        for i in range(x, x+h) :
            for j in range(y, y+w) :
                knights_graph[i][j] = idx

def trap_check(x, y, h, w, k, d, idx) :
    global alive_knights
    global knights

    # 트랩 갯수 카운트
    count = 0
    for i in range(x, x+h) :
        for j in range(y, y+w) :
            if graph[i][j] == 1 :
                count +=1
    # 함정이 체력이상이면 죽음 -> 해당위치 기사 없다고 업데이트 필요
    if k <= count :
        alive_knights[idx] = False

    else :
        # 체력 깎기
        k = k - count
        # 점수 증가
        knights_score[idx] += count

        # 해당 기사 정보 업데이트
        knights[idx] = [x, y, h, w, k, idx]

def move(x, y, h, w, k, d, idx, first_check) :
    global knights
    global alive_knights
    global move_sets

    mx = x + dx[d]
    my = y + dy[d]

    # 기사 높이
    for i in range(mx, mx+h) :
        for j in range(my, my+w) :
            # 가고자 하는곳이 격자 안이고 벽이 아닌 경우
            if 0 <= i < L and 0 <= j < L and graph[i][j] != 2 :

                # 해당 위치에 자기 자신이 아닌 기사가 있는 경우
                if knights_graph[i][j] != - 1 and knights_graph[i][j] != idx and knights_graph[i][j] not in move_sets:

                    # print("다른 n번 기사가 있어요 밀칠께요", knights_graph[i][j])
                    # 다른 n 번 기사 번호
                    idx2 = knights_graph[i][j]
                    x2, y2, h2, w2, k2, idx2 = knights[idx2]
                    # 해당 나이트 밀었던적 있다고 기록
                    move_sets.add(knights_graph[i][j])
                    # 다른 기사야 너도 움직여라
                    check =  move(x2, y2, h2, w2, k2, d, idx2, False)
                    if check == False :
                        # print(i, j, w2)
                        # print("idx에게 idx2 안밀려요", idx, idx2, k2)
                        # print("위치는 여기에요", x2, y2, d)
                        return False

            else :

                # print("격자 밖이거나 벽이라 이동 불가 명령이행 실패")
                return False

    #이동 가능
    # 함정 점수 계산 해야함
    if first_check == False :
        trap_check(mx, my, h, w, k, d, idx)
    else :
        # 첫 기사는 함정 점수 계산안해서 거기거 업데이트 안했음 -> 나이트 그래프도 추가 업데이트 필요
        knights[idx] = [mx, my, h, w, k, idx]
    return True

def attack(num, d) :
    global move_sets


    global alive_knights
    global knights_graph
    global knights
    global knights_score

    temp_live = alive_knights
    temp_graph = knights_graph
    temp_knights = knights
    temp_knights_score = knights_score

    move_sets = set()
    x, y, h, w, k, idx = knights[num]
    move_sets.add(idx)
    # 처음 밀려나가는 친구는 점수 계산 안하기 위함

    check = move(x, y, h, w, k, d, idx, True)
    # 못움직이는 걸로 결론 나면 이전 행동 모두 취소
    if check == False :
        alive_knights = temp_live
        knights_graph = temp_graph
        knights = temp_knights
        knights_score = temp_knights_score




for _ in range(L) :
    graph.append(list(map(int, input().split())))

for idx in range(N) :
    r, c, h, w, k = map(int, input().split())
    knights.append([r-1, c-1, h, w, k, idx])

knights_init()

for _ in range(Q) :
    #해당 기사번호에게 공격방향 명령어
    knight_num, attack_d = map(int, input().split())

    # 해당 기사가 살아있어야 명령 수행
    if alive_knights[knight_num-1] == True :
        attack(knight_num-1, attack_d)
    # 나이트 그래프 다시 재구축
    knights_init()

# 살아 있는 친구들 점수 계산
answer = 0
for i in range(N) :
    if alive_knights[i] == True :
        answer += knights_score[i]
print(answer)