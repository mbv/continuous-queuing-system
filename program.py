from math import log, fabs
from random import random
from matplotlib import pyplot as plt


class Source:
    def __init__(self, intensity):
        self.intensity = intensity
        self.need_time = 0

    def try_get(self, time):
        if time >= self.need_time:
            self.need_time = get_random_time(self.intensity)
            return True
        self.need_time -= time
        return False


class Channel:
    def __init__(self, intensity):
        self.intensity = intensity
        self.need_time = 0
        self.ready = True

    def try_push(self):
        if self.ready:
            self.need_time = get_random_time(self.intensity)
            self.ready = False
            return True
        return False

    def try_get(self, time):
        if not self.ready:
            if time >= self.need_time:
                self.ready = True
                self.need_time = 0
                return True
            else:
                self.need_time -= time
        return False


class Queue:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0

    def try_push(self):
        if self.count < self.max_count:
            self.count += 1
            return True
        return False

    def try_get(self):
        if self.count > 0:
            self.count -= 1
            return True
        return False


def get_random_time(intensity):
    tmp = random()
    if tmp < 0.000000001:
        tmp = 0.000000001
    if tmp > 0.999999999:
        tmp = 0.999999999
    return round(fabs((60. / intensity) * log(tmp)))


def simulate(l, m1, m2, n1, n2, count):
    source = Source(l)
    queue1 = Queue(n1)
    channel1 = Channel(m1)
    queue2 = Queue(n2)
    channel2 = Channel(m2)

    all_time = 0
    time = 0

    otk = 0
    otk1 = 0

    gen = 0

    processed1 = 0
    processed2 = 0

    for _ in range(0, count):
        if channel2.try_get(time):
            processed2 += 1

        if channel2.ready and queue2.try_get():
            channel2.try_push()

        if channel1.try_get(time):
            processed1 += 1
            if not (channel2.try_push() or queue2.try_push()):
                otk += 1

        if channel1.ready and queue1.try_get():
            channel1.try_push()

        if source.try_get(time):
            gen += 1
            if not (channel1.try_push() or queue1.try_push()):
                otk1 += 1

        all_time += time
        time = min(filter(lambda x: x > 0, [source.need_time, channel1.need_time, channel2.need_time]), default=0)

    potk = (otk + otk1)/gen
    potk1 = otk1/gen
    potk2 = otk/processed2

    print("Time: ", all_time)
    print("lambda: ", l)
    print("m1: ", m1, " m2: ", m2)
    print("n1: ", n1, " n2: ", n2)
    print("Potk: ", potk, " Potk1: ", potk1, " Potk2: ", potk2)
    print("***********")
    return [potk, potk1, potk2]


la = 4.5
mu1 = 5
mu2 = 5
n1_from = 1
n1_to = 6

n2 = 2

count = 100000

result = []
for i in range(n1_from, n1_to + 1):
    result.append(simulate(la, mu1, mu2, i, n2, count))

plt.plot(list(range(n1_from, n1_to + 1)), list(map(lambda x: x[0], result)), color='red', label='Potk')
plt.plot(list(range(n1_from, n1_to + 1)), list(map(lambda x: x[1], result)), color='blue', label='Potk1')
plt.plot(list(range(n1_from, n1_to + 1)), list(map(lambda x: x[2], result)), color='green', label='Potk2')
potk, = plt.plot(list(range(n1_from, n1_to + 1)), list(map(lambda x: x[0], result)), 'ro', color='red', label='Potk')
potk1, = plt.plot(list(range(n1_from, n1_to + 1)), list(map(lambda x: x[1], result)), 'ro', color='blue', label='Potk1')
potk2, = plt.plot(list(range(n1_from, n1_to + 1)), list(map(lambda x: x[2], result)), 'ro', color='green', label='Potk2')
plt.legend(handles=[potk, potk1, potk2])
plt.show()
