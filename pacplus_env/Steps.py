from pacplus_env.Actions import Actions

# A = Agent
# C = Computer
# H = Human
# An enurable class used to specify the set of action steps required to perform different predefined tasks
# E.g. changing the story mode difficulty, or starting a new game in single player story mode

def start_game(frame_ratio):
    return [
        {"wait": 50, "actions": [Actions.COIN_P1]},
        {"wait": 60//frame_ratio, "actions": [Actions.P1_START]},
        ]


def new_game(frame_ratio):
    return [{"wait": 150//frame_ratio, "actions": []}] + start_game(frame_ratio)