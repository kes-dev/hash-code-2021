import numpy as np
from collections import OrderedDict, deque

class Car:
    def __init__(self, id, t):
        self.id = id
        self.t = t
        self.curr_path = 0
        self.wait_time = OrderedDict()

class Simulation:
    def __init__(self, map_data, schedules):
        self.streets = map_data.street
        self.trips = map_data.trip
        self.f = map_data.misc.f
        self.d = map_data.misc.d
        self.schedules = schedules
        self.clean()

    def clean(self):
        self.interQueue = {}
        self.green_light = {}
        self.arrived = []

    def run(self):
        # init intersection
        for i, sch in self.schedules.items():
            self.interQueue[i] = {}
            for st_name, green_period in sch.items():
                self.interQueue[i][st_name] = deque()

        # init car
        max_score = 0
        for trip in self.trips:
            st_start = trip.path[0]
            int_start = self.streets[st_start].end
            car = Car(trip.id, 0)
            self.interQueue[int_start][st_start].append(car)

            max_score += self.f + self.d
            for st_name in trip.path[1:]:
                max_score -= self.streets[st_name].length

        print('Max possible score: {}'.format(max_score))

        # sim init
        for i, sch in self.schedules.items():
            st_name, duration = sch.items()[0]
            self.green_light[i] = (0, st_name, duration)

        # sim loop
        for t in range(0, self.d):
            if t % 100 == 0:
                print('tick: {} / {}'.format(t, self.d))
            self.tick(t)

            if len(self.arrived) == len(self.trips):
                print('All cars arrived final destination, ends sim at tick {}'.format(t))
                break

        return self.calc_score(), self.arrived

    def tick(self, t):
        for i, sch in self.schedules.items():
            index, st_name, remain = self.green_light[i]
            if remain == 0:
                index = (index + 1) % len(sch.keys())
                st_name, duration = sch.items()[index]
                self.green_light[i] = (index, st_name, duration - 1)
            else:
                self.green_light[i] = (index, st_name, remain - 1)

            if len(self.interQueue[i][st_name]) > 0:
                self.pass_intersection(st_name, i, t)

    def pass_intersection(self, st_name, i, t):
        diff = t - self.interQueue[i][st_name][0].t
        if diff >= 0:
            car = self.interQueue[i][st_name].popleft()
            car.curr_path += 1

            if len(self.trips[car.id].path) > car.curr_path:
                dest_name = self.trips[car.id].path[car.curr_path]
                dest = self.streets[dest_name]

                car.wait_time[st_name] = diff
                car.t = t + dest.length

                self.interQueue[dest.end][dest_name].append(car)

            else:
                self.arrived.append(car)

    def calc_score(self):
        score = self.f * len(self.arrived)
        for car in self.arrived:
            score += self.d - car.t
        return score
