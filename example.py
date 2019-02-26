import random
from pacplus_env.Environment import Environment
import time

t = time.time()

roms_path = "roms/"  # Replace this with the path to your ROMs
env = Environment("env1", roms_path, frame_ratio=3, frames_per_step=3)
env.start()
print("Game loaded in",time.time() - t,"seconds.")

count_death = 0
is_alive = False
last_action = -1

score = 0

while True:
    if not is_alive:
        print("Waiting for reboot")
        env.wait_until_move()
        print("You can now move")

    move_action = random.randint(0, 4)

    if not last_action == -1 and random.random() < .5:
        move_action = last_action

    frames, reward, is_alive = env.step(move_action)
    last_action = move_action
    score += reward

    print("Score:", score,"\tReward:",reward)

    if not is_alive:
        print("Pac-Man is Dead :(")
        count_death += 1
        last_action = -1

    if count_death == 3:
        print("Let's try again")
        env.new_game()
        count_death = 0
        score = 0
        print("Next game")