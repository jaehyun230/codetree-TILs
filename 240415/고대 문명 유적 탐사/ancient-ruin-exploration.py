from collections import deque
import copy


K, M = map(int, input().split())

graph =[]

for _ in range(5) :
    graph.append(list(map(int, input().split())))

blocks = list(map(int, input().split()))

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def refill() :
    global index
    for j in range(5):
        for i in reversed(range(5)):
            if graph[i][j] == 0:
                graph[i][j] = blocks[index]
                index +=1

def rotate_90(start_x, start_y, size, data_graph) :

    temp = [[0]*5 for _ in range(5)]

    for i in range(start_x, start_x+size) :
        for j in range(start_y, start_y+size) :
            ox, oy = i-start_x, j-start_y
            rx, ry = oy, size-1-ox

            temp[start_x+rx][start_y+ry] = data_graph[i][j]

    for i in range(start_x, start_x + size):
        for j in range(start_y, start_y + size):
            data_graph[i][j] = temp[i][j]

    return data_graph


def score_cal(data_graph) :
    q = deque()

    visited = [[False]*5 for _ in range(5)]

    temp_blocks = []

    for i in range(5) :
        for j in range(5) :
            if visited[i][j] == False :
                temp = []
                q.append([i, j, data_graph[i][j]])
                temp.append([i, j])
                visited[i][j] = True

                while q :
                    nx, ny, value = q.popleft()

                    for k in range(4) :
                        mx = nx + dx[k]
                        my = ny + dy[k]

                        if 0 <= mx < 5 and 0 <= my < 5 and visited[mx][my] == False :

                            if data_graph[mx][my] == value :
                                visited[mx][my] = True
                                temp.append([mx, my])
                                q.append([mx, my, value])

                if len(temp) >= 3 :
                    temp_blocks.append(temp)

    scores = 0

    for b in temp_blocks :
        scores += len(b)

    return scores

def calculate(x, y) :

    result_score, result_rotate_count = -1, -1

    temp_graph = copy.deepcopy(graph)

    temp_graph = rotate_90(x, y, 3, temp_graph)
    score1 = score_cal(temp_graph)
    if score1 > result_score :
        result_score = score1
        result_rotate_count = 1

    temp_graph = rotate_90(x, y, 3, temp_graph)
    score2 = score_cal(temp_graph)

    if score2 > result_score :
        result_score = score2
        result_rotate_count = 2

    temp_graph = rotate_90(x, y, 3, temp_graph)
    score3 = score_cal(temp_graph)

    if score3 > result_score :
        result_score = score3
        result_rotate_count = 3

    return result_score, result_rotate_count


def find_rotate_pos() :
    result_x, result_y, result_rotate_count, result_score = 0, 0, 1, 0
    for i in range(3) :
        for j in range(3) :
            score, rotate_count = calculate(i, j)
            if score > result_score :
                result_x, result_y, result_rotate_count, result_score = i, j, rotate_count, score

            elif score == result_score and result_rotate_count > rotate_count :
                result_x, result_y, result_rotate_count, result_score = i, j, rotate_count, score

            elif score == result_score and result_rotate_count == rotate_count and result_y > j :
                result_x, result_y, result_rotate_count, result_score = i, j, rotate_count, score

            elif score == result_score and result_rotate_count == rotate_count and result_y == j and result_x > i :
                result_x, result_y, result_rotate_count, result_score = i, j, rotate_count, score

    return result_x, result_y, result_rotate_count


def real_rotate(x, y, count) :
    global graph
    temp_graph = copy.deepcopy(graph)

    for i in range(count) :
        temp_graph = rotate_90(x, y, 3, temp_graph)
    # 회전한값으로 업데이트
    graph = temp_graph

def real_score_cal() :
    global graph
    q = deque()

    visited = [[False]*5 for _ in range(5)]

    temp_blocks = []

    for i in range(5) :
        for j in range(5) :
            if visited[i][j] == False :
                temp = []
                q.append([i, j, graph[i][j]])
                temp.append([i, j])
                visited[i][j] = True

                while q :
                    nx, ny, value = q.popleft()

                    for k in range(4) :
                        mx = nx + dx[k]
                        my = ny + dy[k]

                        if 0 <= mx < 5 and 0 <= my < 5 and visited[mx][my] == False :

                            if graph[mx][my] == value :
                                visited[mx][my] = True
                                temp.append([mx, my])
                                q.append([mx, my, value])

                if len(temp) >= 3 :
                    temp_blocks.append(temp)

    scores = 0

    for b in temp_blocks :
        scores += len(b)

    for bb in temp_blocks :
        for x, y in bb :
            graph[x][y] = 0

    return scores


time = 0
index = 0
while time < K :
    answer = 0
    result_x, result_y, result_rc = find_rotate_pos()

    real_rotate(result_x, result_y, result_rc)
    first_score = real_score_cal()

    if first_score == 0 :
        break
    answer +=first_score

    while True :
        refill()
        score = real_score_cal()
        if score == 0 :
            break
        answer += score

    print(answer, end =" ")

    time +=1