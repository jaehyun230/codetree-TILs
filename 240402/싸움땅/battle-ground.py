import sys
import heapq

n, m, k = map(int, input().split())

guns = [
    [[] for _ in range(n)] for _ in range(n)]

score = [0] * m
players = []

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for i in range(n) :
    data = list(map(int, input().split()))
    for j in range(n) :
        heapq.heappush(guns[i][j], -1 * data[j])

for i in range(m) :
    x, y, d, s = map(int ,input().split())
    players.append((i, x-1, y-1, d, s, 0))

def update(player) :
    idx, x, y, d, s, w = player

    for i in range(m):
        num, _, _, _, _, _ = players[i]
        if idx == num:
            players[i] = player
            break
    
def check_player_exist(a, b) :
    for i in range(len(players)) :
        idx, x, y, d, s, w = players[i]
        if a == x and b == y :
            return players[i]
    
    return [-1, -1, -1, -1, -1, -1]

def lose(player) :
    idx, x, y, d, s, w = player

    for i in range(4) :
        md = d + i
        mx = x + dx[i]
        my = y + dy[i]
        if 0 <= mx < n and 0 <= my < n :
            p2 = check_player_exist(mx, my)
            if p2[0] == -1 :
                p = idx, mx, my, md, s, w
                move(p)
                break

def win(player, player2) :
    
    idx, x, y, d, s, w = player
    idx2, x2, y2, d2, s2, w2 = player2
    score[idx] += (s+w) - (s2+w2)
    
    dropgun(player)
    getgun(player)

def fight(player1, player2) :
    idx, x, y, d, s, w = player1
    idx2, x2, y2, d2, s2, w2 = player2
    
    if (s+w) > (s2+w2) :
        # 진사람이 떨어진 총 주워야 할 수도 있기 때문
        lose(player2)
        win(player1, player2)
    elif (s+w) == (s2+w2) :
        if s > s2 :
            lose(player2)
            win(player1, player2)
        else :
            lose(player1)
            win(player2, player1)
    else :
        lose(player1)
        win(player2, player1)

def dropgun(player) :
    idx, x, y, d, s, w = player
    if w != 0 :
        heapq.heappush(guns[x][y], -1*w)
        w = 0
    p = (idx, x, y, d, s, w)
    update(p)

def getgun(player) :
    idx, x, y, d, s, w = player
    if guns[x][y] :
        gun = heapq.heappop(guns[x][y]) * -1
        w = gun
    p = (idx, x, y, d, s, w)
    update(p)

def move(player) :
    dropgun(player)
    getgun(player)
    
    #현재 이동 위치에 총 확인


def play() :
    for i in range(len(players)) :
        # 번호, (x, y)좌표, 방향, 기초스텟, 총
        idx, x, y, d, s, w = players[i]

        if 0 <= x + dx[d] < n and 0 <= y + dy[d] < n :
            p = ((idx, x+dx[d], y+dy[d], d, s, w))
            p2 = check_player_exist(x+dx[d], y+dy[d])
            if p2[0] != -1 :
                fight(p, p2)
            else :
                move(p)
        else :
            # 반대 방향 이동
            d = (d+2)%4
            if 0 <= x + dx[d] < n and 0 <= y + dy[d] < n :
                p = ((idx, x+dx[d], y+dy[d], d, s, w))
                p2 = check_player_exist(x+dx[d], y+dy[d])
                if p2[0] != -1 :
                    fight(p, p2)
                else :
                    move(p)
        
for _ in range(k) :
    play()

for i in range(m) :
    print(score[i], end =" ")