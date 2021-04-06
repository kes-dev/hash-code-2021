import argparse
import yaml
from datetime import datetime

import datautil as du
import strategy.naiveratio as nr
from sim import Simulation
import poststat

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
    print('Cars: {}'.format(misc.trip_count))
    print('Bonus: {}'.format(misc.f))

def print_score(score, arrived, total):
    print('Score: {}'.format(score))
    print('Arrived/Total: {} / {}'.format(arrived, total))

def log_section(msg, time=None):
    rPad = 80
    time = datetime.now() if time == None else time
    print(('{} {} '.format(time, msg)).ljust(rPad, '='))

def main():
    log_section('Run Start')
    log_section('Prepare Config')
    cfg = prepare_config()
    print(cfg)

    dm = du.DataManager(cfg['map_path'], cfg['schedule_path'], cfg['result_path'])
    dm.check_path()

    log_section('Load Map Data')
    map_data = dm.load_map()
    print_map_info(map_data.misc)

    log_section('Generate Schedule')
    schedule = gen_schedule(cfg['strategy'], map_data)
    dm.save_schedule(schedule)

    sim = Simulation(map_data, schedule)
    start_time = datetime.now()
    log_section('Simulation Starts', start_time)

    score, arrived = sim.run()

    end_time = datetime.now()
    log_section('Simulation Ends', end_time)

    print('Simulation took: {} '.format(end_time - start_time))

    dm.save_result(score, arrived)
    print_score(score, len(arrived), map_data.misc.trip_count)

    #poststat.wait_time_dist_by_order(arrived)
    #poststat.wait_time_dist_by_intersection(map_data.street, schedule, arrived)

    log_section('Run End')

if __name__ == "__main__":
    main()
