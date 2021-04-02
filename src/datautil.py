class Street:
    def __init__(self, begin, end, length):
        self.begin = begin
        self.end = end
        self.length = length

class Car:
    def __init__(self, str_count, paths):
        self.str_count = str_count
        self.paths = paths

class Intersection:
    def __init__(self, incoming=None, outgoing=None, schedule=None):
        self.incoming = incoming if incoming != None else []
        self.outgoing = outgoing if outgoing != None else []
        self.schedule = schedule if schedule != None else {}

    def validate(self, schedule):
        for st, _ in schedule:
            assert st in incoming == True

class Misc:
    def __init__(self, d, int_count, str_count, car_count, f):
        self.d = d
        self.int_count = int_count
        self.str_count = str_count
        self.car_count = car_count
        self.f = f

class MapData:
    def __init__(self, misc, street, car):
        self.misc = misc
        self.street = street
        self.car = car

class DataManager:
    def __init__(self, map_path, schedule_path):
        self.map_path = map_path
        self.schedule_path = schedule_path

    def check_path(self):
        assert os.path.exists(self.map_path) == True
        if (os.path.exists(self.schedule_path)):
            print("WARN: schedule output path exists!  Will overwrite!")
            print(self.schedule_path)

    def load_map(self):
        street = {}
        car = []

        with open(self.map_path, 'r') as f:
            for index, line in enumerate(f.readlines()):
                line = line.rstrip('\n')
                if index == 0:
                    d, int_count, str_count, car_count, f = line.split(' ')
                    misc = Misc(int(d), int(int_count), int(str_count), int(car_count), int(f))

                elif index <= misc.str_count:
                    begin, end, name, length = line.split(' ')
                    street[name] = Street(int(begin), int(end), int(length))

                else:
                    str_count, *paths = line.split(' ')
                    c = Car(int(str_count), paths)
                    car.append(c)

        assert len(street) == misc.str_count
        assert len(car) == misc.car_count
        return MapData(misc, street, car)

    def save_schedule(self, schedule):
        with open(self.schedule_path, 'w') as f:
            for i, sch in enumerate(schedule):
                f.write(str(i) + '\n')
                f.write(str(len(sch.keys())) + '\n')
                for st_name, green_duration in sch.items():
                    f.write('{} {}'.format(st_name, green_duration) + '\n')

    def load_schedule(self):
        print('load_schedule Not yet implemented!')
