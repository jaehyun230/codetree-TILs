from collections import defaultdict

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

n = int(input())

graph = [[0] *n for _ in range(n)]

dic = defaultdict(list)

def seat_check(x, y, lover) :

    #주변에 자신이 좋아하는 사람 수
    myfriend = 0
    # 빈칸 수
    blank = 0

    for i in range(4) :
        mx = x + dx[i]
        my = y + dy[i]

        if 0<= mx < n and 0 <= my < n :
            if graph[mx][my] == 0 :
                blank +=1
            elif graph[mx][my] in lover :
                myfriend +=1

    return myfriend, blank

def find_favorite(info) :

    pos = [-1, -1]
    friend_count, blank_count = -1, -1

    for i in range(n) :
        for j in range(n) :
            # 빈자리 일 경우
            if graph[i][j] == 0 :
                f_c, b_c = seat_check(i, j, info)
                if friend_count < f_c :
                    friend_count, blank_count = f_c, b_c
                    pos = [i, j]
                elif friend_count == f_c and blank_count < b_c :
                    friend_count, blank_count = f_c, b_c
                    pos = [i, j]

    return pos


def point_score(x, y) :
    global answer

    my_num = graph[x][y]
    f_count = 0
    data = dic[my_num]

    for i in range(4) :
        mx = x + dx[i]
        my = y + dy[i]
        if 0<= mx < n and 0 <= my < n :
            if graph[mx][my] in data :
                f_count +=1

    if f_count == 2:
        f_count = 10
    elif f_count == 3:
        f_count = 100
    elif f_count == 4:
        f_count = 1000
    answer +=f_count

def total_score() :
    for i in range(n) :
        for j in range(n) :
            point_score(i, j)



answer = 0

for _ in range(n**2) :
    a, b, c, d, e = map(int, input().split())
    #추후에 스코어 계산 하기위한 사전
    dic[a].append(b)
    dic[a].append(c)
    dic[a].append(d)
    dic[a].append(e)

    people_data = [b, c, d, e]
    pos = find_favorite(people_data)
    # 가장 적합한 위치 찾은곳에 사람 나두기
    graph[pos[0]][pos[1]] = a

total_score()
print(answer)