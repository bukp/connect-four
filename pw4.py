from random import choice

class board:
    
    def __init__(self, grid = None, turn = 1):
        self.player = turn
        if grid == None:
            self.grid = [["." for _ in range(8)] for _ in range(8)]
        else :
            self.grid = grid
        self.size = len(self.grid)
    
    def __repr__(self):
        out = ""
        out += "".join([" "+str(i+1) for i in range(len(self.grid))])+"\n"
        out += "".join([" v" for i in range(len(self.grid))])+"\n"
        for i in self.grid:
            for j in i:
                out += " "+ j
            out += "\n"
        return out
        
    def __getitem__(self, key):
        return self.grid[key[1]][key[0]]

    def copy(self):
        return board([[j for j in i] for i in self.grid], self.player)
    
    def can_play(self, col):
        return list(map(lambda x: x[col-1], self.grid)).count(".") != 0

    def play(self, col):
        if list(map(lambda x: x[col-1], self.grid)).count(".") == 0:
            raise Exception(f"Cannot play on col {col}")
        self.grid[list(map(lambda x: x[col-1], self.grid)).count(".")-1][col-1] = "O" if self.player == 1 else "X"
        self.player = self.player%2+1
    
    def state(self):
        slices = []
        for i in range(len(self.grid)):
            slices.append("".join(map(lambda x: x[i-1], self.grid)))
            slices.append("".join(self.grid[i]))
            slices.append("".join(map(lambda x: self.grid[i+x][x], range(len(self.grid)-i))))
            slices.append("".join(map(lambda x: self.grid[x][x+i], range(len(self.grid)-i))))
            slices.append("".join(map(lambda x: self.grid[len(self.grid)-1-x][x+i], range(len(self.grid)-i))))
            slices.append("".join(map(lambda x: self.grid[len(self.grid)-1-x-i][x], range(len(self.grid)-i))))
        for i in slices:
            if "OOOO" in i:
                return 1
            elif "XXXX" in i:
                return 2
        return 0
    
    def static_eval(self):
        slices = []
        for i in range(len(self.grid)):
            slices.append("".join(map(lambda x: x[i-1], self.grid)))
            slices.append("".join(self.grid[i]))
            slices.append("".join(map(lambda x: self.grid[i+x][x], range(len(self.grid)-i))))
            slices.append("".join(map(lambda x: self.grid[x][x+i], range(len(self.grid)-i))))
            slices.append("".join(map(lambda x: self.grid[len(self.grid)-1-x][x+i], range(len(self.grid)-i))))
            slices.append("".join(map(lambda x: self.grid[len(self.grid)-1-x-i][x], range(len(self.grid)-i))))
        eval = 0
        if self.state() == 0:
            for slc in slices:
                if "OO." in slc:
                    eval += 2
                if ".OO" in slc:
                    eval += 2
                if "OOO." in slc or ".OOO" in slc:
                    eval += 10
                if "XX." in slc:
                    eval -= 1
                if ".XX" in slc:
                    eval -= 2
                if "XXX." in slc or ".XXX" in slc:
                    eval -= 10
            return eval
        else :
            return float("inf") if self.state() == 1 else float("-inf")

    def eval(self, n = 4):
        if n == 0 :
            return (None, self.static_eval())
        elif self.state() != 0:
            return (None, self.static_eval())
        else :
            if self.player == 1:
                best = (0, float("-inf"))
                for i in range(1, self.size+1):
                    copy = self.copy()
                    if copy.can_play(i):
                        copy.play(i)
                        test = (i, copy.eval(n-1)[1])
                        if test[1] >= best[1]:
                            best = test
                return best
            else :
                best = (0, float("inf"))
                for i in range(1, self.size+1):
                    copy = self.copy()
                    if copy.can_play(i):
                        copy.play(i)
                        test = (i, copy.eval(n-1)[1])
                        if test[1] <= best[1]:
                            best = test
                return best

if __name__ == "__main__":
    brd = board()
    print(brd)
    while True:
        brd.play(int(input(">> ")))
        if brd.state() != 0:
            print(f"Player {brd.state()} won")
            break
        brd.play(brd.eval()[0])
        if brd.state() != 0:
            print(brd)
            print(f"Player {brd.state()} won")
            break
        print(brd)