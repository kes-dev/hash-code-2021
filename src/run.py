import argparse
import yaml

import datautil as du
import strategy.naiveratio as nr

def prepare_config():
    parser = argparse.ArgumentParser(description='traffic simulation')
    parser.add_argument('-c', '--cfg', help='File path config file', required=True)
    args = parser.parse_args()

    with open(args.cfg, 'r') as cfg_file:
        return yaml.load(cfg_file, Loader=yaml.FullLoader)

def gen_schedule(strategy, map_data):
    if strategy['name'] == 'naiveratio':
        nr.validate(strategy['config'])
        return nr.gen_schedule(map_data, strategy['config'])

def print_map_info(misc):
    print('Duration: {}'.format(misc.d))
    print('Intersections: {}'.format(misc.int_count))
    print('Streets: {}'.format(misc.str_count))
    print('Cars: {}'.format(misc.car_count))
    print('Bonus: {}'.format(misc.f))

def log_section(msg):
    rPad = 40
    print(('{} '.format(msg)).ljust(rPad, '='))

def main():
    log_section('Run Start')
    log_section('Prepare Config')
    cfg = prepare_config()
    print(cfg)

    dm = du.DataManager(cfg['map_path'], cfg['schedule_path'])

    log_section('Load Map Data')
    map_data = dm.load_map()
    print_map_info(map_data.misc)

    log_section('Generate Schedule')
    schedule = gen_schedule(cfg['strategy'], map_data)

    log_section('Save Schedule')
    dm.save_schedule(schedule)

    log_section('Gather Schedule Statistics')


    log_section('Run Simulation')

    log_section('Evaluate')

    log_section('Run End')

if __name__ == "__main__":
    main()
