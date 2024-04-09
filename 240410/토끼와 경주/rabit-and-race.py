import heapq
from collections import defaultdict

# 모든 토끼가 얻는 점수로 계산하고 점프한 토끼만 점수얻는거 뺴기
all_score = 0

N = int(input())

data = list(map(int, input().split()))

# n*m판 p마리토끼
n, m, p =  data[1], data[2], data[3]


# 경기 중 뽑현던 토끼 고려하기
# 처음 토끼들은 전부 1행, 1열
rabbit = []
# 토끼 뽑는 우선 순위는 총점프 횟수 낮은애 , 현재 행 + 열 낮은 애, 행 낮은애, 열 낮은애, 고유번호 낮은 애
# 추가로 들어갈 데이터는 이동거리 d

# 이동거리 배수
rabbit_speed = {}

#토끼 점수 저장
score = {}

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for i in range(2, p+2) :
    pid, d = data[2*i], data[2*i+1]

    # 토끼 이동거리 배수 1배(기본값)
    rabbit_speed[pid] = 1
    # 토끼 초기 점수
    score[pid] = 0

    heapq.heappush(rabbit, (0, 0, 0, 0, pid, d))

def outOfRange(nx, ny):
    nx %= 2 * (n - 1)
    ny %= 2 * (n - 1)

    return min(nx, 2*(n - 1) - nx), min(ny, 2*(m - 1) - ny)
def jump(x, y, pid, d) :
    #토끼 점프하며 움직여볼까요~
    total_d = d * rabbit_speed[pid]

    result_x, result_y = -1, -1

    for i in range(4) :
        ddx = dx[i]*total_d
        ddy = dy[i]*total_d

        mx = x + ddx
        my = y + ddy

        if not 0 <= mx < n :
            mx , _ =outOfRange(mx, my)
        if not 0 <= my < m :
            _ , my = outOfRange(mx, my)

        if mx + my > result_x+result_y :
            result_x, result_y = mx, my
        elif mx + my == result_x +result_y and mx > result_x :
            result_x, result_y = mx, my
        elif mx + my == result_x + result_y and mx == result_x and my > result_y :
            result_x, result_y = mx, my

    return [result_x, result_y]

def play(k, s) :
    # all_score 떄 실제 행렬 1,1 시작이라 +2 항상 해줘야함
    global all_score

    count = 0

    # 이번 게임 경기 중 점프한 토끼 모음 - pid key 다음 밑 우선 순위로
    temp_jump_rabbit = defaultdict(list)

    winner_row_col, winner_row, winner_col, winner_pid = -1, -1, -1, -1

    # k 번 게임 반복
    while count < k :

        jump_rabbit = heapq.heappop(rabbit)
        jump_count, row_col, row, col, pid, d = jump_rabbit
        pos = jump(row, col, pid, d)
        # - pos 값 가져오고 raabit heapq 푸쉬
        heapq.heappush(rabbit, (jump_count+1, pos[0]+pos[1], pos[0], pos[1], pid, d))
        # 점프 후 매번 temp_jump_raabit pid키로 값 갱신
        temp_jump_rabbit[pid] = [pos[0]+pos[1], pos[0], pos[1], pid]
        # 점프 한애 뺴고 모두 점수 흑득
        all_score += pos[0] + pos[1] + 2
        score[pid] -= pos[0] + pos[1] + 2

        count +=1

    # k 번 반복 후 뛰었던 토끼들 중 (현재 서있는 행 번호 + 열 번호가 큰 토끼, 행 번호가 큰 토끼, 열 번호가 큰 토끼, 고유번호가 큰 토끼) -> s 점수 흑득
    for rabbit_pid in temp_jump_rabbit :
        row_col, row, col, pid, = temp_jump_rabbit[rabbit_pid]
        if winner_row_col < row_col :
            winner_row_col, winner_row, winner_col, winner_pid = row_col, row, col, pid
        elif winner_row_col == row_col and winner_row < row :
            winner_row_col, winner_row, winner_col, winner_pid = row_col, row, col, pid
        elif winner_row_col == row_col and winner_row == row and winner_col < col :
            winner_row_col, winner_row, winner_col, winner_pid = row_col, row, col, pid
        elif winner_row_col == row_col and winner_row == row and winner_col == col and winner_pid < pid :
            winner_row_col, winner_row, winner_col, winner_pid = row_col, row, col, pid
    score[winner_pid] +=s


for _ in range(N-2) :
    q, a, b = map(int, input().split())

    if q == 200 :
        play(a, b)
    # 명령어 300 일떄 해당 pid(a) 토끼 이동거리 b배
    if q == 300 :
        rabbit_speed[a] *=b

#400 input
input()

max_score = 0
#경기 한적 없다면
if not score :
    print(0)
else :
    for pid in score :
        max_score = max(max_score, all_score+score[pid])

    print(max_score)