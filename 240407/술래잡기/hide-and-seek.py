n, m, h, k = map(int, input().split())
center = n // 2

runner = []
runner_alive = [True] * m

graph = [[0] * n for _ in range(n)]
trees = [[0] * n for _ in range(n)]

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for idx in range(m):
    x, y, d = map(int, input().split())

    runner.append([x - 1, y - 1, d, idx])

for _ in range(h):
    a, b = map(int, input().split())
    trees[a - 1][b - 1] = 1

time = 1

# 술래 위치, 방향, 방향전환까지 남은 걸음 수, 이전 방향전환 필요 걸음 수, 방향전환 카운트(2번 방향전환후 걸음수 +1), /순방향-0 역방향-1
target = (center, center, 0, 1, 1, 2, 0)

def update(a, b, c, d, e, f, g):
    global target
    target = ((a, b, c, d, e, f, g))


# 역방향 고려 필요 이후
def target_move():
    x, y, d, need_d, next_d, count, check = target

    # 순방향일 경우 이동 상태

    # 바라보는 방향으로 이동
    mx = x + dx[d]
    my = y + dy[d]
    need_d -= 1

    if mx == 0 and my == 0:
        check = 1
        d = (d + 2) % 4
        next_d -=1
        need_d = next_d
        count = 3

    elif mx == center and my == center:
        check = 0
        d = (d + 2) % 4
        next_d = 1
        need_d = 1
        count = 2

    elif need_d == 0:
        if check == 1 :
            d = (d-1) %4
        else :
            d = (d + 1) % 4

        count -= 1
        if count == 0 and check == 0:
            next_d += 1
            count = 2
        elif count == 0 and check == 1:
            next_d -= 1
            count = 2

        need_d = next_d

    update(mx, my, d, need_d, next_d, count, check)


def catch():
    global answer
    x, y, d, _, _, _, _ = target

    for num in range(3):
        mx = x + dx[d] * num
        my = y + dy[d] * num
        if 0 <= mx < n and 0 <= my < n and trees[mx][my] == 0:
            for run in runner:
                x2, y2, d2, idx = run
                # 해당위치와 살아 있는 경우
                if x2 == mx and y2 == my and runner_alive[idx] == True:
                    runner_alive[idx] = False
                    answer += time

def update_runner(a, b, c, d):
    runner[d] = [a, b, c, d]

def runner_move():
    for run in runner:
        x, y, d, idx = run

        # 죽은사람 경우 pass
        if runner_alive[idx] == False:
            continue
        # 거리가 3 이내 일 경우 이동
        if abs(target[0] - x) + abs(target[1] - y) <= 3:

            mx = x + dx[d]
            my = y + dy[d]
            if 0 <= mx < n and 0 <= my < n:
                # 술래 위치라면 이동 안하기
                if mx == target[0] and my == target[1]:
                    continue
                else:
                    update_runner(mx, my, d, idx)
            else:
                d = (d + 2) % 4
                mx = x + dx[d]
                my = y + dy[d]
                if mx == target[0] and my == target[1]:
                    update_runner(x, y, d, idx)
                else:
                    update_runner(mx, my, d, idx)


answer = 0
while time < k + 1:
    runner_move()
    target_move()
    catch()
    time += 1

print(answer)