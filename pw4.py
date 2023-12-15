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
        
    def eval(self, n):
        if self.state() == 0:
            if n == 0:
                return 0
            else :
                outcome = []
                for i in range(1, self.size+1):
                    test = board.copy(self)
                    if not test.can_play(i):
                        outcome.append(None)
                    else :
                        test.play(i)
                        outcome.append(test.eval(n-1))
                if self.player in outcome:
                    return self.player
                elif 0 in outcome:
                    return 0
                else :
                    return self.player%2+1
        else :
            return self.state()

    def choose(self, n = 3):
        outcome = []
        for i in range(1, self.size+1):
            test = board.copy(self)
            if not test.can_play(i):
                outcome.append(None)
            else :
                test.play(i)
                outcome.append(test.eval(n))
        print(outcome)
        if self.player in outcome:
            return choice([i for i in range(len(outcome)) if outcome[i] == self.player]) + 1
        elif 0 in outcome:
            return choice([i for i in range(len(outcome)) if outcome[i] == 0]) + 1
        else :
            return choice([i for i in range(len(outcome)) if outcome[i] == self.player%2+1]) + 1

if __name__ == "__main__":
    brd = board()
    while True:
        brd.play(int(input(">> ")))
        if brd.state() != 0:
            print(f"Player {brd.state()} won")
            break
        brd.play(brd.choose())
        if brd.state() != 0:
            print(brd)
            print(f"Player {brd.state()} won")
            break
        print(brd)