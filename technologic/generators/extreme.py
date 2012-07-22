def extreme(duration):

    time = 0
    data = []

    while time <= duration:

        if time <= 1:
            data.append({time: time + 10})

        time = time + .1

    return data