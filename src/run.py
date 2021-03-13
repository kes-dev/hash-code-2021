import logging
import argparse
import yaml

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
            chunks = str.split(' ')
            if index == 0:
                misc['duration'] = chunks[0],
                misc['intersection'] = chunks[1],
                misc['street'] = chunks[2],
                misc['car'] = chunks[3],
                misc['bonus'] = chunks[4]

            elif index <= misc['streetCount']:
                street_curr = {
                    'begin': chunk[0],
                    'end': chunk[1],
                    'name': chunk[2],
                    'length': chunk[3]
                }
                street.append(street_curr)
            else:
                car_curr = {
                    'streets': chunks[0],
                    'path': chunks[1:]
                }
                car.append(car_curr)

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
    logging.info(trip_data['misc'])
    logging.info(trip_data['street'])
    logging.info(trip_data['car'])

    logging.info('---load schedule data---')
    schedule_data = load_schedule(cfg['schedule_data_path'])

    logging.info('---run simulation---')

    logging.info('---evaluate---')

    logging.info('---run end---')

if __name__ == "__main__":
    main()
