
class Nonogram:
    def __init__(self, row_clues, col_clues):
        self.row_clues = row_clues #row is Hang
        self.col_clues = col_clues
        self.grid_size = len(row_clues)
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
    def draw_grid(self):
        st = ''
        for j in self.col_clues :
            st = st + str(j) + ' '
        st += '\n'
        for i in range(self.grid_size):
            
            for j in range(self.grid_size):
                if self.grid[i][j] == 1:
                    st += '#'
                elif self.grid[i][j] == 0:
                    st += '0'
                else :
                    st += 'X'
            st += ":" + str(self.row_clues[i])
            st += '\n'
        
        # Draw clues (not interactive, just for display)
        return st
    def solve(self, row_num):
        
        if row_num > self.grid_size:
            col_num = row_num - self.grid_size - 1
            possible_pos = []
            ck_num = 0
            for i in range(self.grid_size):
                if self.grid[i][col_num] == 0:
                    ck_num += 1
            if ck_num ==0:
                return
            
            def dfs(lis):
                l = len(lis)
                if l>5:
                    if cksub(lis) == False:
                        return
                if l == self.grid_size:
                    ck(lis)
                else:
                    if self.grid[l][col_num] == 0:
                        dfs(lis+[-1])
                        dfs(lis+[1])
                    else :
                        dfs(lis+[self.grid[l][col_num]])
            def cksub(lis):
                pnt = 0
                pre = 0
                for i in lis:
                    if i == 1:
                        pre = pre+1
                    elif pre > 0:
                        if pnt == len(self.col_clues[col_num]):
                            return False
                        if pre != self.col_clues[col_num][pnt]:
                            return False
                        pnt = pnt + 1
                        pre = 0
                return True
                
            def ck(lis):
                pnt = 0
                pre = 0
                lis.append(-1)
                for i in lis:
                    if i == 1:
                        pre = pre+1
                    elif pre > 0:
                        if pnt == len(self.col_clues[col_num]):
                            return
                        if pre != self.col_clues[col_num][pnt]:
                            return
                        pnt = pnt + 1
                        pre = 0
    
                if pnt == len(self.col_clues[col_num]):
                    possible_pos.append(lis[:-1])
            dfs([])
            decision = [ int(sum(elements)/len(possible_pos)) for elements in zip(*possible_pos)]
            for i in range(self.grid_size):
                if self.grid[i][col_num]==0:
                    self.grid[i][col_num] += decision[i]
            #self.grid[row_num] = [sum(elem) for elem in zip(decision,self.grid[row_num])]
            return 
            
        row_num -= 1
        ck_num = 0
        for i in range(self.grid_size):
            if self.grid[row_num][i] == 0:
                ck_num += 1
        if ck_num ==0:
            return
        possible_pos = []

        def dfs(lis):
            l = len(lis)
            if l>5:
                if cksub(lis) == False:
                    return
            if l == self.grid_size:
                ck(lis)
            else:
                if self.grid[row_num][l] == 0:
                    dfs(lis+[-1])
                    dfs(lis+[1])
                else :
                    dfs(lis+[self.grid[row_num][l]])

        def cksub(lis):
            pnt = 0
            pre = 0
            for i in lis:
                if i == 1:
                    pre = pre+1
                elif pre > 0:
                    if pnt == len(self.row_clues[row_num]):
                        return False
                    if pre != self.row_clues[row_num][pnt]:
                        return False
                    pnt = pnt + 1
                    pre = 0
            return True
            
        def ck(lis):
            pnt = 0
            pre = 0
            lis.append(-1)
            for i in lis:
                if i == 1:
                    pre = pre+1
                elif pre > 0:
                    if pnt == len(self.row_clues[row_num]):
                        return
                    if pre != self.row_clues[row_num][pnt]:
                        return
                    pnt = pnt + 1
                    pre = 0

            if pnt == len(self.row_clues[row_num]):
                possible_pos.append(lis[:-1])
        dfs([])
        decision = [ int(sum(elements)/len(possible_pos)) for elements in zip(*possible_pos)]
        for i in range(self.grid_size):
            if self.grid[row_num][i]==0:
                self.grid[row_num][i] += decision[i]
    def is_solve(self):
        for i in self.grid:
            for j in i :
                if j == 0:
                    return False
        return True




def generate_entry(rin):
    lis = [[int(j) for j in i.split('.')] for i in rin.split('/')]
    l = len(lis)//2
    A = Nonogram(lis[:l],lis[l:])
    res = ''
    res += str(lis[:l]) + '\n'
    res += str(lis[l:]) + '\n\n'
    res += A.draw_grid()
    i = 1
    while A.is_solve() == False:
        if i <= A.grid_size:
            res += 'R'+str(i) + ':\n'
            A.solve(i)
        else:
            res += 'C'+str(i - A.grid_size) + ':\n'
            A.solve(i)
        res += A.draw_grid()
        if i == 2*A.grid_size:
            i = 0
        i += 1
    res += ']]'
    return {"text": res}


import requests
import re
#https://cn.puzzle-nonograms.com/?size=1
url = 'https://www.puzzle-nonograms.com/?size=0'
a = requests.get(url)
match = re.search(r"var task = '([^']*)'", a.text)
# Extract the content within the quotes if the pattern is found
task_value = match.group(1) if match else None
print(generate_entry(task_value)['text'])
