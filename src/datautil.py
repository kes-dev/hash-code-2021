class Street:
    def __init__(self, begin, end, length):
        self.begin = begin
        self.end = end
        self.length = length

class Trip:
    def __init__(self, str_count, path, id):
        self.str_count = str_count
        self.path = path
        self.id = id

class Intersection:
    def __init__(self, id, incoming=None, outgoing=None):
        self.id = id
        self.incoming = incoming if incoming != None else []
        self.outgoing = outgoing if outgoing != None else []

class Misc:
    def __init__(self, d, int_count, str_count, trip_count, f):
        self.d = d
        self.int_count = int_count
        self.str_count = str_count
        self.trip_count = trip_count
        self.f = f

class MapData:
    def __init__(self, misc, intersection, street, trip):
        self.misc = misc
        self.intersection = intersection
        self.street = street
        self.trip = trip

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
        inter = []
        street = {}
        trip = []
        trip_id = 0

        with open(self.map_path, 'r') as f:
            for index, line in enumerate(f.readlines()):
                line = line.rstrip('\n')
                if index == 0:
                    d, int_count, str_count, trip_count, f = line.split(' ')
                    misc = Misc(int(d),
                                int(int_count),
                                int(str_count),
                                int(trip_count),
                                int(f))

                    for i in range(0, misc.int_count):
                        inter.append(Intersection(i))

                elif index <= misc.str_count:
                    begin, end, name, length = line.split(' ')
                    street[name] = Street(int(begin), int(end), int(length))
                    inter[int(end)].incoming.append(name)
                    inter[int(begin)].outgoing.append(name)

                else:
                    str_count, *path = line.split(' ')
                    trip.append(Trip(int(str_count), path, trip_id))
                    trip_id += 1

        assert len(inter) == misc.int_count
        assert len(street) == misc.str_count
        assert len(trip) == misc.trip_count

        return MapData(misc, inter, street, trip)

    def save_schedule(self, schedules):
        with open(self.schedule_path, 'w') as f:
            for i, sch in schedules.items():
                f.write(str(i) + '\n')
                f.write(str(len(sch.keys())) + '\n')
                for st_name, green_duration in sch.items():
                    f.write('{} {}'.format(st_name, green_duration) + '\n')

    def load_schedule(self):
        print('load_schedule Not yet implemented!')
