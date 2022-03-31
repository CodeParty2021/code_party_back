import enum
from player import Player
from field import Field
import random
import json
import sys
import io


class Option:
    def __init__(
        self,
        width: int = 5,
        height: int = 5,
        num_players: int = 4,
        initial_pos=[(0, 0), (0, 4), (4, 4), (4, 0)],
        max_turn=30,
        initial_field=None,
        json_path=None,
        user_code=None,
        players=None,
    ):
        self.width = width
        self.height = height
        self.num_players = num_players
        self.initial_pos = initial_pos
        self.max_turn = max_turn
        self.initial_field = initial_field  # NoneのときFieldのコンストラクタで初期化
        self.json_path = json_path
        self.players = players
        if len(initial_pos) != num_players:
            raise Exception("initial_posとnum_playersの数が合ってません")

        def ret_ERROR(state):
            return 5

        if user_code == None:
            user_code = [ret_ERROR for i in range(num_players)]
        if players == None:
            players = [
                {"name": "デモ太郎", "icon": "https://sample.com"}
                for i in range(num_players)
            ]
        self.user_code = user_code


def reduceDim(list):
    ret = []
    for l in list:
        ret = ret + l
    return ret


def start(option: Option = Option()):
    # フィールド生成
    field = Field(option)

    # プレイヤー生成
    players = [Player(i, option) for i in range(option.num_players)]

    # 最初の足場に色を塗る
    for player in players:
        field.color(player.get_pos(), player.id, players)

    # scoreの初期値を設定
    scores = judge(option, field.mask_field())["scores"]
    for player, score in zip(players, scores):
        player.set_score(score)

    # json用の辞書を生成
    json_ = {
        "players": option.players,
        "stage": {
            "width": option.width,
            "height": option.height,
            "field": reduceDim(field.mask_field()),
            "players": [
                {"x": player.pos_x, "y": player.pos_y, "score": player.score}
                for player in players
            ],
        },
        "turn": [],
        "result": {},
    }
    # シミュレーション実行
    run(option.max_turn, field, players, option.user_code, json_)

    # 結果測定
    # print(judge(option,field.mask_field()))
    json_["result"] = judge(option, field.mask_field())

    # JSON出力
    if option.json_path is not None:
        save_json(option, json_)
    return json_


def get_states(players, field):
    masked_field = field.mask_field()
    others = [players[: player.id] + players[player.id + 1 :] for player in players]
    return [
        {
            "my_pos": player.get_pos(),
            "others_pos": [other.get_pos() for other in others[player.id]],
            "field": masked_field,
        }
        for player in players
    ]


def get_next_actions(players, states, user_code):
    ret_list = []
    for player, state, code in zip(players, states, user_code):
        # 文字列IOストリームを初期化して、f に代入
        with io.StringIO() as f:
            # 標準出力を f に切り替える。
            sys.stdout = f

            # actionを実行
            action = player.action(state, code)

            # f に出力されたものを文字列として取得
            text = f.getvalue()

            # 標準出力をデフォルトに戻して text を表示
            sys.stdout = sys.__stdout__
            ret_list += [{"action": action, "print": text}]
    return ret_list


def step(next_actions, field, players):
    # next_actionを実行しfieldとplayerのフィールドを更新

    # 1.各プレイヤーの座標を更新
    for player, action in zip(players, next_actions):
        player.step(action)

        # 復帰１ターン前に座標更新
        if player.state == Player.FALL1:
            player.set_pos(field.get_random_pos())

        # 復帰処理
        if player.state == Player.REVIVED:
            player.state = Player.SAFE

    # 色を塗れないプレイヤーはリストから消していく
    coloring_players = [player for player in players]

    # 2.衝突判定
    pos = {}
    for player in players:
        p_pos = player.get_pos()
        if p_pos in pos:
            pos[p_pos] += [player]
        else:
            pos[p_pos] = [player]
    # 衝突している場合，1人以外は色を塗らない
    for splited_players in pos.values():
        num = len(splited_players)
        if num >= 2:
            elected = random.randrange(num)
            for player in splited_players[:elected] + splited_players[elected + 1 :]:
                coloring_players.remove(player)
    # 3.落下判定
    for player in players:
        if player.is_safe() and field.is_fall(player.get_pos()):
            player.fall()
            if player in coloring_players:
                coloring_players.remove(player)

        if not player.is_safe():
            if player in coloring_players:
                coloring_players.remove(player)
    # 4.色塗り
    for player in coloring_players:
        field.color(player.get_pos(), player.id, players)


def check_finish():
    # 終了条件を満たしたかを返す
    # 現状max_turnのみ
    return False


def debug(msg):
    if __debug__:
        # print(msg)
        pass


def debug_log(players, field):
    if __debug__:
        for player in players:
            print(
                "player"
                + str(player.id)
                + ":"
                + str(player.get_pos())
                + " "
                + str(player.state)
            )
        for line in field.field[::-1]:
            for c in line:
                view = "　"
                if c == -1:
                    view = "⚪"
                elif c == 0:
                    view = "０"
                elif c == 1:
                    view = "１"
                elif c == 2:
                    view = "２"
                elif c == 3:
                    view = "３"

                print(view, end="")
            print()


def run(max_turn: int, field: Field, players: list, user_code: list, json: dict):
    # debug("初期状態")
    # debug_log(players,field)
    for i in range(max_turn):
        # 現在のフィールドを保存

        player_states = [
            {
                "x": player.pos_x,
                "y": player.pos_y,
                "state": player.state,
            }
            for player in players
        ]

        # 4人分の状態を生成
        states = get_states(players, field)
        """
        下の辞書が人数分入った辞書が作られる
        {
            "my_pos":(1,1),
            "other_pos":[(2,2),(3,3),(4,4)]
            "field":int[][]
        }
        """
        # 4人分の行動を収集
        # actionに行動，printに標準出力が入った辞書を4人分のリストにして返ってくる
        action_results = get_next_actions(players, states, user_code)

        for j, result in enumerate(action_results):
            player_states[j]["action"] = result["action"]

        next_actions = [result["action"] for result in action_results]
        prints = [result["print"] for result in action_results]

        # 行動を反映
        step(next_actions, field, players)

        # 終了時の処理
        if check_finish():
            break

        # JSONへ保存
        # debug(str(i+1)+"ターン目の処理後")
        # debug_log(players,field)

        ## scoreをplayer_stateに追加
        for i, player in enumerate(players):
            player_states[i]["score"] = player.score

        ## printsをplayer_stateに追加
        for i, text in enumerate(prints):
            player_states[i]["print"] = text

        turn_info = {
            "field": reduceDim(field.mask_field()),  # unityの仕様上1次元化する
            "players": player_states,
        }
        json["turn"].append(turn_info)


def judge(option, field):
    # fieldsの要素を数える
    score = []
    for i in range(option.num_players):
        score += [0]

    for line in field:
        for value in line:
            if 0 <= value < option.num_players:
                score[value] += 1
    idx_list = [(s, i) for i, s in enumerate(score)]

    idx_list.sort(reverse=True)

    return {"scores": score, "rank": [i for s, i in idx_list]}


def save_json(option, dict):
    with open(option.json_path, "w") as f:
        json.dump(dict, f, indent=4)


if __debug__:
    start()
