import winsound
import time

def play_result_sound(hit, blow):
    # Hitは高い音
    for _ in range(hit):
        winsound.Beep(1000, 200)
        time.sleep(0.05)

    # Blowは低い音
    for _ in range(blow):
        winsound.Beep(600, 200)
        time.sleep(0.05)