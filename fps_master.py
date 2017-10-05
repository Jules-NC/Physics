import time


def regulate_fps(method, fps=30):
    time_gap = 1 / fps
    prem_time = time.time()
    i = 0
    while True:
        first_time = time.time()

        method()

        #i += 1
        # if time.time() - prem_time > 1:
        #     print('FPS: ', i)
        #     i = 0
        #     prem_time = time.time()

        second_time = time.time()
        if second_time-first_time < time_gap:
            ab = first_time+time_gap-first_time
            ac = time.time() - first_time
            time.sleep(ab-ac)  # Processor optimisation
        else:
            print('|=========[ALERT]==========|')
            print('FPS_NON_OPTIMISES')
            time.sleep(5)


def random_process():
    print(time.time())


if  __name__ == '__main__':
    regulate_fps(random_process, fps=1000)