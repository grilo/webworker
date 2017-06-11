#!/usr/bin/env python

import sys
import logging
import argparse

import bottle

import utils


if __name__ == '__main__':
    if sys.version_info < (2,6) or sys.version_info > (2,8):
        raise SystemExit('Sorry, this code needs Python 2.6 or Python 2.7 (current: %s.%s)' % (sys.version_info[0], sys.version_info[1]))

    desc = 'Extracts data using the multiple drivers and posts data to elasticsearch.'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-v', '--verbose', action='store_true', \
        help='Increase output verbosity')
    parser.add_argument('-t', '--host', default='localhost', \
        help='The host where the application will listen in.')
    parser.add_argument('-p', '--port', default='8080', \
        help='The port where the web server will listen to.')

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s::%(levelname)s::%(message)s')
    logging.getLogger().setLevel(getattr(logging, 'INFO'))

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('Verbose mode activated.')

    app = bottle.Bottle()

    # Dynamically load all modules
    for inspector in utils.load_inspectors():
        route_path = '/' + inspector.__name__
        verbs = ['GET', 'POST', 'PUT', 'DELETE']
        for verb in verbs:
            if hasattr(inspector, verb):
                app.route(route_path, verb, getattr(inspector, verb))
                app.route(route_path + '/<item>', verb, getattr(inspector, verb))

    app.run(host=args.host, port=args.port, debug=args.verbose, reloader=args.verbose)
