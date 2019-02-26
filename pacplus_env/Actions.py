from enum import Enum
from MAMEToolkit.emulator.Action import Action


# An enumerable class used to specify which actions can be used to interact with a game
# Specifies the Lua engine port and field names required for performing an action
class Actions(Enum):
    # Starting
    SERVICE =   Action(':IN1', 'Service Mode')

    COIN_P1 =   Action(':IN0', 'Coin 1')
    COIN_P2 =   Action(':IN0', 'Coin 2')

    P1_START =  Action(':IN1', '1 Player Start')
    P2_START =  Action(':IN1', '2 Players Start')

    # Movement
    P1_UP =     Action(':IN0', 'P1 Up')
    P1_DOWN =   Action(':IN0', 'P1 Down')
    P1_LEFT =   Action(':IN0', 'P1 Left')
    P1_RIGHT =  Action(':IN0', 'P1 Right')

    P2_UP =     Action(':IN1', 'P2 Up')
    P2_DOWN =   Action(':IN1', 'P2 Down')
    P2_LEFT =   Action(':IN1', 'P2 Left')
    P2_RIGHT =  Action(':IN1', 'P2 Right')

    # Other
    RACK_TEST =     Action(':IN0',  'Rack Test (Cheat)')
    LIVES =         Action(':DSW1', 'Lives')
    COINAGE =       Action(':DSW1', 'Coinage')
    GHOST_NAMES =   Action(':DSW1', 'Ghost Names')
    BONUS_LIFE =    Action(':DSW1', 'Bonus Life')
    DIFFICULTY =    Action(':DSW1', 'Difficulty')
    CABINET =       Action(':IN1',  'Cabinet')