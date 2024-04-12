from collections import defaultdict
N = int(input())

graph = [[0]*N for _ in range(N)]

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

love_dic = defaultdict(list)

def find_my_pos(a, b, c, d, e) :

    result_x, result_y = -1, -1
    result_love, result_bin = -1, -1

    for i in range(N) :
        for j in range(N) :
            # 빈 공간일 경우 해당 위치 점수 계산
            if graph[i][j] == 0 :
                love = 0
                bin = 0
                for k in range(4) :
                    mx = i + dx[k]
                    my = j + dy[k]

                    if 0 <= mx < N and 0 <= my < N :
                        if graph[mx][my] == b or graph[mx][my] == c or graph[mx][my] == d or graph[mx][my] == e :
                            love +=1

                        elif graph[mx][my] == 0 :
                            bin +=1

                if love > result_love :
                    result_x, result_y = i, j
                    result_love, result_bin = love, bin
                elif love == result_love and bin > result_bin :
                    result_x, result_y = i, j
                    result_love, result_bin = love, bin

    # 최종적으로 찾은 위치에 그래프 값 나두기
    graph[result_x][result_y] = a

for _ in range(N**2) :
    l, l1, l2, l3, l4 = map(int, input().split())
    find_my_pos(l, l1, l2, l3, l4)
    love_dic[l].append(l1)
    love_dic[l].append(l2)
    love_dic[l].append(l3)
    love_dic[l].append(l4)

answer = 0
for i in range(N) :
    for j in range(N) :
        love_count = 0
        me = graph[i][j]

        for k in range(4) :
            mx = i + dx[k]
            my = j + dy[k]

            if 0 <= mx < N and 0 <= my < N :
                if graph[mx][my] in love_dic[me] :
                    love_count +=1

        if love_count == 2:
            answer +=10
        elif love_count ==3 :
            answer +=100
        elif love_count == 4 :
            answer +=1000
        else :
            answer +=love_count
print(answer)