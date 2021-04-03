from queue import PriorityQueue

class Car:
    def __init__(self, id, t, path):
        self.id = id
        self.t = t
        self.path = path

def run(map_data, schedule):
    # init intersection
    interQueue = []
    for i, sch in enumerate(schedule):
        interQueue.append({})
        setattr(sch, 'period', 0)

        for st_name, green_period in sch.items():
            interQueue[i][st_name] = []
            sch.period += green_period

    # init car
    for trip in map_data.trip:
        st_start = trip.path[0]
        int_start = map_data.street[st_start].end
        car = Car(trip.id, 0, trip.path[1:])
        interQueue[int_start][st_start].append(car)

    arrived = []
    for t in range(0, map_data.misc.d):
        interQueue, arrived = tick(map_data.street, interQueue, schedule, arrived, t)
        print('tick: {}'.format(t))

    return calc_score(map_data.misc.d, map_data.misc.f, arrived)

def tick(street_data, interQueue, schedule, arrived, t):
    for i, sch in enumerate(schedule):
        if sch.period == 0:
            continue

        remain = t % sch.period
        for st_name, green_duration in sch.items():
            remain -= green_duration
            if remain <= 0 and len(interQueue[i][st_name]) > 0:
                car = interQueue[i][st_name][0]
                if car.t < t:
                    del interQueue[i][st_name][0]

                    if len(car.path) > 0:
                        st_name = car.path[0]
                        dest = street_data[st_name]
                        del car.path[0]
                        car.t = t + dest.length
                        interQueue[dest.end][st_name].append(car)
                    else:
                        arrived.append(car)

                break
    return interQueue, arrived

def calc_score(d, f, arrived):
    score = f * len(arrived)
    for car in arrived:
        score += d - car.t
    return score
