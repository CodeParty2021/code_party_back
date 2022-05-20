import traceback


class Player:
    UP, RIGHT, DOWN, LEFT, STAY, ERROR, FALL = 0, 1, 2, 3, 4, 5, 6
    SAFE, FALL1, FALL2, FALL3, REVIVED = 0, 1, 2, 3, 4

    def __init__(self, id, option) -> None:
        self.id = id
        self.pos_x, self.pos_y = option.initial_pos[id]
        self.state = self.SAFE
        self.score = 0

    def action(self, state, user_code=None):
        if self.state == self.SAFE:
            if not user_code:
                return self.UP
            try:
                output = user_code(state["turn_num"],state["field"], state["my_pos"], state["others_pos"])
                if(self.validate(output)):
                    return user_code(state["turn_num"],state["field"], state["my_pos"], state["others_pos"])
                else:
                    raise Exception("[0,1,2,3,4] のどれかを返してください")
            except Exception as e:
                print(traceback.format_exc())
                return self.ERROR
        return self.FALL

    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def set_pos(self, pos):
        self.pos_x, self.pos_y = pos

    def step(self, action):
        if self.state == self.SAFE:
            if action == self.UP:
                self.pos_y += 1
            elif action == self.DOWN:
                self.pos_y -= 1
            elif action == self.RIGHT:
                self.pos_x += 1
            elif action == self.LEFT:
                self.pos_x -= 1
            elif action == self.STAY or action == self.ERROR:
                pass
        elif self.state == self.FALL3:
            self.state = self.FALL2
        elif self.state == self.FALL2:
            self.state = self.FALL1
        elif self.state == self.FALL1:
            self.state = self.REVIVED

    def fall(self):
        self.state = self.FALL3

    def is_safe(self):
        return self.state == self.SAFE

    def set_score(self, score):
        self.score = int(score)

    def add(self, increment):
        self.score += increment

    def validate(self,output):
        return output in [0,1,2,3,4]