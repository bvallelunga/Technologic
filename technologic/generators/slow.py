from random import randint

def slow(duration):

    time = 0.0000
    data = []
    def random(max = 10):
            return randint(0, max)

    while time <= duration:

        if time < 1:
            data.append({time: int(time) + random(50)})

        if 1<= time <= 10:
            data.append({time: int(time) + random(50)})


        time = time + .5

    return data