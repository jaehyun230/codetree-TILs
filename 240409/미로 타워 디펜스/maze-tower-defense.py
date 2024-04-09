n, m = map(int, input().split())

graph = []

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

for _ in range(n) :
    graph.append(list(map(int, input().split())))

# 포탑은 중앙에서 위치
center = n//2

def destroy(data) :
    global answer

    # 중복 갯수
    count = 0
    value = -1
    start_pos = -1
    end_pos = -1
    for i in range(len(data)) :

        # 4개이상인 상태에서는 뺴고 return 하게 설정하기
        if value != data[i] :

            if count >=4 :
                answer += count*value
                return True, (start_pos, end_pos)

            value = data[i]
            count = 1
            start_pos = i

        elif value == data[i] :
            count +=1
            end_pos = i

    if count >= 4 :
        answer += count * value
        return True, (start_pos, end_pos)

    return False, (start_pos, end_pos)

# 달팽이 회전 순서 왼 아래 오른 상향
def rotation_point() :

    global answer

    # 시작 방향 왼쪽
    d = 2
    # 방향 전환 까지 남은 횟수
    need_d = 1
    # need_d 다음 필요 걸음수
    next_d = 1
    # 2번마다 걸음 수 필요 걸음 수 1 증가
    count = 2

    x, y = center, center

    # 그냥 스택에 다 쌓은 다음 하면 되지않을까?
    stack = []

    for _ in range(n**2):

        x, y = x + dx[d], y + dy[d]

        need_d -= 1
        if need_d == 0:
            d = (d - 1) % 4
            count -= 1
            if count == 0:
                count = 2
                next_d += 1

            need_d = next_d

        if 0 <= x < n and 0 <= y < n and graph[x][y] > 0 :
            stack.append(graph[x][y])

    # 스택에 다 쌓은 상태 4개 이상일 경우 삭제
    # print(stack)
    # print(stack)
    while True :
        check, posdata = destroy(stack)

        if check == False :
            break
        stack = stack[:posdata[0]] + stack[posdata[1] + 1::]



    return stack

# 달팽이 모양 돌아서 확인하는 프로그램
def rotation_check() :

    # 시작 방향 왼쪽
    d = 2
    # 방향 전환 까지 남은 횟수
    need_d = 1
    # need_d 다음 필요 걸음수
    next_d = 1
    # 2번마다 걸음 수 필요 걸음 수 1 증가
    count = 2

    x, y = center, center

    # 그냥 스택에 다 쌓은 다음 하면 되지않을까?

    for _ in range(n**2) :

        x, y = x + dx[d], y + dy[d]

        need_d -= 1
        if need_d == 0 :
            d = (d-1)%4
            count -=1
            if count == 0 :
                count = 2
                next_d +=1

            need_d = next_d

        if 0 <= x < n and 0 <= y < n :
            print(graph[x][y], end = " ")

def attack(d, p) :
    global answer

    graph[center][center]

    for i in range(1, p+1) :
        mx = center + dx[d]*i
        my = center + dy[d]*i

        if 0 <= mx < n and 0 <= my < n and graph[mx][my] > 0 :
            answer += graph[mx][my]
            graph[mx][my] = 0

# 남은 데이터로 다시 작업하기
def remodell(data) :

    temp = []
    temp2 = []
    value = -1
    for i in range(len(data)) :
        if value != data[i] :
            if len(temp2) != 0 :
                temp.append(temp2)
                temp2 = []

            temp2.append(data[i])
            value = data[i]
        else :
            temp2.append(data[i])

    temp.append(temp2)

    return temp

def reconstruct(data) :
    global graph

    # 시작 방향 왼쪽
    d = 2
    # 방향 전환 까지 남은 횟수
    need_d = 1
    # need_d 다음 필요 걸음수
    next_d = 1
    # 2번마다 걸음 수 필요 걸음 수 1 증가
    count = 2

    x, y = center, center

    # 들어갈 데이터
    indata = []
    # print(data)

    for i in range(len(data)) :
        indata.append(len(data[i]))
        indata.append(data[i][0])

    temp = [[0]*n for _ in range(n)]

    # 그냥 스택에 다 쌓은 다음 하면 되지않을까?

    for i in range(len(indata)) :

        x, y = x + dx[d], y + dy[d]

        need_d -= 1
        if need_d == 0 :
            d = (d-1)%4
            count -=1
            if count == 0 :
                count = 2
                next_d +=1

            need_d = next_d

        if 0 <= x < n and 0 <= y < n :
            temp[x][y] = indata[i]

        if x == 0 and y == 0 :
            break

    graph = temp

answer = 0
for _ in range(m) :
    # 공격 방향 및 칸수
    d, p = map(int, input().split())
    attack(d, p)
    remain = rotation_point()
    redata = remodell(remain)
    reconstruct(redata)

print(answer)