from MAMEToolkit.emulator.Emulator import Emulator
from MAMEToolkit.emulator.Address import Address
from pacplus_env.Steps import *
from pacplus_env.Actions import Actions

# Returns the list of memory addresses required to train on Pac-Man Plus
def setup_memory_addresses():
    return {
        "score0": Address('0x00004E80', 'u8'),
        "score1": Address('0x00004E81', 'u8'),
        "score2": Address('0x00004E82', 'u8'),
        "score3": Address('0x00004E83', 'u8'),
        "lives" : Address('0x00004E14', 'u8'),
        "coins" : Address('0x00004E6E', 'u8'),
        "status": Address('0x00004EAE', 'u8')
    }


# Converts and index (action) into the relevant movement action Enum, depending on the player
def index_to_move_action(action):
    return {
        0: [Actions.P1_LEFT],
        1: [Actions.P1_UP],
        2: [Actions.P1_RIGHT],
        3: [Actions.P1_DOWN],
        4: []
    }[action]

# The Pac-Man Plus specific interface for training an agent against the game
class Environment(object):

    # env_id - the unique identifier of the emulator environment, used to create fifo pipes
    # difficulty - the difficult to be used in story mode gameplay
    # frame_ratio, frames_per_step - see Emulator class
    # render, throttle, debug - see Console class
    def __init__(self, env_id, roms_path, frame_ratio=3, frames_per_step=3, render=True, throttle=False, debug=False, cheat_debugger=False):
        self.frame_ratio = frame_ratio
        self.frames_per_step = frames_per_step
        self.throttle = throttle
        self.emu = Emulator(env_id, roms_path, "pacplus", setup_memory_addresses(), frame_ratio=frame_ratio, render=render, throttle=throttle, debug=debug, cheat_debugger=cheat_debugger)
        self.started = False
        self.is_alive = False
        self.prev_score = 0

    # Runs a set of action steps over a series of time steps
    # Used for transitioning the emulator through non-learnable gameplay, aka. title screens, character selects
    def run_steps(self, steps):
        for step in steps:
            for i in range(step["wait"]):
                self.emu.step([])
            self.emu.step([action.value for action in step["actions"]])

    # Must be called first after creating this class
    # Sends actions to the game until the learnable gameplay starts
    # Returns the first few frames of gameplay
    def start(self):
        if self.throttle:
            for i in range(int(100/self.frame_ratio)):
                self.emu.step([])
        self.run_steps(start_game(self.frame_ratio))
        self.started = True
        return self.gather_frames([])

    def new_game(self):
        self.run_steps(new_game(self.frame_ratio))
        self.prev_score = 0
        self.is_alive = False
        return self.wait_until_move()

    def wait_until_move(self):
        data = self.emu.step([])
        while data["status"] == 0:
            data = self.emu.step([])
        self.is_alive = True

    # Collects the specified amount of frames the agent requires before choosing an action
    def gather_frames(self, actions):
        data = self.sub_step(actions)
        frames = [data["frame"]]
        for i in range(self.frames_per_step - 1):
            frames.append(data["frame"])
        data["frame"] = frames[0] if self.frames_per_step == 1 else frames
        return data

    # Steps the emulator along by one time step and feeds in any actions that require pressing
    # Takes the data returned from the step and updates book keeping variables
    def sub_step(self, actions):
        data = self.emu.step([action.value for action in actions])

        score = data["score0"]//16 * 10 + (data["score1"]%16) * 100 + data["score1"]//16 * 1000 + (data["score2"]%16) * 10000 + data["score2"]//16 * 100000 + (data["score3"]%16) * 1000000 + data["score3"]//16 * 10000000
        data["reward"] = score - self.prev_score
        self.prev_score = score

        return data

    # Steps the emulator along by the requested amount of frames required for the agent to provide actions
    def step(self, move_action):
        if self.started:
            if self.is_alive:
                actions = []
                actions += index_to_move_action(move_action)
                data = self.gather_frames(actions)

                lives = data["lives"]

                nb_coins = data["coins"]

                self.is_alive = data["status"] != 0

                return data["frame"], data["reward"], self.is_alive
            else:
                raise EnvironmentError("Attempted to step while pause")
        else:
            raise EnvironmentError("Start must be called before stepping")

    # Safely closes emulator
    def close(self):
        self.emu.close()
