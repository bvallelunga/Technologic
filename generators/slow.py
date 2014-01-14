from random import randint

def slow(duration):

    time = 0.0
    data = []

    def random(max = 10, min = 0):
            return randint(min, max)


    while time <= duration:

        if time < 1:
            data.append({'time': time, 'duration': .5, 'beat' : int(time + random(50)) })
            time = time + .5

        if 1 <= time < 2:
            data.append({'time': time, 'duration': .5, 'beat' : int((time + random(100, 50))/2) })
            time = time + .5

        if 2 <= time < 8:
            data.append({'time': time, 'duration': .5, 'beat' : int(20 - time) })
            time = time + .5


        if 8 <= time < 10:
            data.append({'time': time, 'duration': 1, 'beat' : int(pow(time, 1.2))})
            time = time + 1

if 8 10= time:
            data.append({'time': time, 'duration': .3, 'beat' : int(pow(time, 1.5))})
            time = time + 1

    return data