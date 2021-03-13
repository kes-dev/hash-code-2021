import logging
import argparse
import yaml
import importlib.util
spec = importlib.util.spec_from_file_location("sim", "./sim.py")
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
foo.MyClass()

logging.basicConfig(filename='run.log',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO)

def prepare_config():
    parser = argparse.ArgumentParser(description='traffic simulation')
    parser.add_argument('-c', '--cfg', help='File path config file', required=True)
    args = parser.parse_args()

    with open(args.cfg, 'r') as cfg_file:
        return yaml.load(cfg_file, Loader=yaml.FullLoader)

def load_trip(path):
    misc = {}
    street = []
    car = []

    with open(path, 'r') as trip_data_file:
        for index, line in enumerate(trip_data_file.readlines()):
            chunks = line.split(' ')
            if index == 0:
                misc['duration'] = int(chunks[0])
                misc['intersection'] = int(chunks[1])
                misc['street'] = int(chunks[2])
                misc['car'] = int(chunks[3])
                misc['bonus'] = int(chunks[4])

            elif index <= misc['street']:
                street_curr = {
                    'begin': int(chunks[0]),
                    'end': int(chunks[1]),
                    'name': chunks[2],
                    'length': int(chunks[3])
                }
                street.append(street_curr)
            else:
                car_curr = {
                    'streets': int(chunks[0]),
                    'path': chunks[1:]
                }
                car.append(car_curr)

    assert len(street) == misc['street']
    assert len(car) == misc['car']

    trip_data = {}
    trip_data['misc'] = misc
    trip_data['street'] = street
    trip_data['car'] = car

    return trip_data


def load_schedule(path):
    with open(path, 'r') as schedule_data_file:
        logging.info('loadded schedule')

def main():
    logging.info('---run start---')
    logging.info('---prepare configs---')
    cfg = prepare_config()
    logging.info(cfg)

    logging.info('---load trip data---')
    trip_data = load_trip(cfg['trip_data_path'])
    logging.info('map info: ')
    logging.info(trip_data['misc'])

    logging.info('---load schedule data---')
    schedule_data = load_schedule(cfg['schedule_data_path'])

    logging.info('---run simulation---')

    logging.info('---evaluate---')

    logging.info('---run end---')

if __name__ == "__main__":
    main()
