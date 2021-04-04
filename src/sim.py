from collections import OrderedDict

class Car:
    def __init__(self, id, t, path):
        self.id = id
        self.t = t
        self.path = path
        self.wait_time = OrderedDict()


def run(map_data, schedules):
    # init intersection
    interQueue = {}
    for i, sch in schedules.items():
        interQueue[i] = {}
        setattr(sch, 'period', 0)

        for st_name, green_period in sch.items():
            interQueue[i][st_name] = []
            sch.period += green_period

    # init car
    for trip in map_data.trip:
        st_start = trip.path[0]
        int_start = map_data.street[st_start].end
        car = Car(trip.id, 0, trip.path[1:])
        if int_start in interQueue:
            interQueue[int_start][st_start].append(car)

    # sim loop
    arrived = []
    for t in range(0, map_data.misc.d):
        if t % 100 == 0:
            print('tick: {}'.format(t))
        interQueue, arrived = tick(map_data.street, interQueue, schedules, arrived, t)

        if len(arrived) == map_data.misc.trip_count:
            print('All cars arrived final destination, ends sim at tick {}'.format(t))
            break

    score = calc_score(map_data.misc.d, map_data.misc.f, arrived)
    return score, arrived

def tick(street_data, interQueue, schedules, arrived, t):
    for i, sch in schedules.items():
        remain = t % sch.period
        for st_name, green_duration in sch.items():
            remain -= green_duration
            if remain <= 0 and len(interQueue[i][st_name]) > 0:
                car = interQueue[i][st_name][0]
                if car.t <= t:
                    del interQueue[i][st_name][0]

                    if len(car.path) > 0:
                        dest_name = car.path[0]
                        dest = street_data[dest_name]

                        car.wait_time[dest_name] = t - car.t
                        car.t = t + dest.length

                        del car.path[0]
                        if dest.end in interQueue:
                            interQueue[dest.end][dest_name].append(car)
                    else:
                        arrived.append(car)

                break
    return interQueue, arrived

def calc_score(d, f, arrived):
    score = f * len(arrived)
    for car in arrived:
        score += d - car.t
    return score
