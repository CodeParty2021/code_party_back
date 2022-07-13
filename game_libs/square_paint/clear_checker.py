class ClearChecker:
    def __init__(self, clear_rule):
        self.clear_rule = clear_rule
        self.judge_fn, self.flag_mean = self.create_judge_fn(clear_rule)
        self.flag = False

    def check(self, field, pos):
        if self.flag:
            return True
        self.flag = self.judge_fn(field, pos)
        return self.flag

    def result(self):
        return self.flag == self.flag_mean

    def create_judge_fn(self, clear_rule):
        if not clear_rule:
            return self.judge_none, True
        if clear_rule["type"] == "reach":
            self.dst = clear_rule["payload"]["dst"]
            return self.judge_reach, True
        elif clear_rule["type"] == "fill":
            self.N = clear_rule["payload"]["N"]
            return self.judge_fill, True
        elif clear_rule["type"] == "drop":
            return self.judge_drop, False
        raise Exception("定義されていないクリア条件:type=" + clear_rule)

    def judge_reach(self, field, pos):
        return pos == self.dst

    def judge_fill(self, field, pos):
        c = 0
        for line in field:
            for value in line:
                if value == 0:
                    c += 1
        return c >= self.N

    def judge_none(self, field, pos):
        return True

    def judge_drop(self, field, pos):
        return field[pos[1] - 1][pos[0] - 1] != -2
