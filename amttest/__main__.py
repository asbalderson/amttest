#!/usr/bin/env python3

import argparse

from .amttest import AMT_TEST, config_app, setup_logging

def main():
    parser = argparse.ArgumentParser(description='Launch a API with routes for '
                                                 'a test application')
    parser.add_argument('-d', '--debug',
                        help='turn on the debug flag',
                        default=False,
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='turn on terminal output',
                        default=False,
                        action='store_true')
    args = parser.parse_args()
    setup_logging(args.debug, args.verbose)
    config_app(__name__)
    AMT_TEST.run(debug=args.debug)


if __name__ == '__main__':
    main()