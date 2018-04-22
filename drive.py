#!/usr/bin/env/python3
import argparse
import os
from time import time, sleep

import derp.state
import derp.util

def loop(state, controller, components):
    state['timestamp'] = time()
    state['warn'] = 0

    # Sense Plan Act Record loop
    for component in components:
        component.sense()
    controller.plan()
    for component in components:
        component.act()
    state.record()


def main(args):
    car_config_path = os.path.join(os.environ['DERP_ROOT'], 'config', args.config + '.yaml')
    car_config = derp.util.load_config(car_config_path)
    controller_config = derp.util.load_config(args.controller)

    state = derp.state.State(config)
    components = derp.util.load_components(car_config, state)
    controller = derp.util.load_controller(controller_config, state, car_config)

    while not state.done():
        loop(state, controller, components)

        if not args.quiet:
            print("%.3f %.2f %s %s | speed %6.3f + %6.3f %i | steer %6.3f + %6.3f %i" %
                  (state['timestamp'], state['warn'],
                   'R' if state['record'] else '_', 'A' if state['auto'] else '_',
                   state['speed'], state['offset_speed'], state['use_offset_speed'],
                   state['steer'], state['offset_steer'], state['use_offset_steer']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--car', type=str, default=derp.util.get_hostname(),
                        help="location of config file for vehicle")
    parser.add_argument('--controller', type=str, default=None):
                        help="location of controller folder")
    parser.add_argument('--quiet', action='store_true', default=False,
                        help="do not print speed/steer")
    parser.add_argument('--debug', action='store_true', default=False,
                        help="don't encapsulate everything in a try-except")
    args = parser.parse_args()
    main(args)
