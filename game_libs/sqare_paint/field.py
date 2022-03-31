import random

class Field:
    EMPTY = -1
    FALL = -2

    def __init__(self, option):
        self.width = option.width
        self.height = option.height
        self.field = option.initial_field
        if(self.field == None):
            self.generate_field()

    def generate_field(self):
        self.field = [[self.EMPTY]*(self.width+2) for i in range(self.height+2)]
        for i in range(self.width+2):
            self.field[0][i]=self.FALL
            self.field[self.height+1][i]=self.FALL
        for i in range(self.height+2):
            self.field[i][0]=self.FALL
            self.field[i][self.width+1]=self.FALL
    def mask_field(self):
        return [x[1:self.width+1] for x in self.field[1:self.height+1]]

    def rotate_field(self):
        return list(map(list, zip(*self.field)))[::-1]

    def get_value(self,pos):
        return self.field[pos[1]+1][pos[0]+1]

    def set_value(self,pos,v):
        self.field[pos[1]+1][pos[0]+1] = v

    def is_fall(self,pos):
        return self.get_value(pos)==self.FALL

    def color(self,pos,id,players):
        if(self.get_value(pos)==self.FALL):
            raise Exception("FALLに塗ろうとしました")
        
        #playerのscoreを更新
        before = self.get_value(pos)
        if(before>=0):
            players[before].add(-1)
        if(id>=0):
            players[id].add(1)
        
        #fieldの色を変更
        self.set_value(pos,id)


    def get_random_pos(self):
        return (random.randrange(self.width),random.randrange(self.height))