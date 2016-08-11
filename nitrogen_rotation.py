#!/usr/bin/env python3
__author__ = "Christoph Rist"
__copyright__ = "Copyright 2016, Christoph Rist"
__license__ = "MIT"

# read/write own config file
import yaml
# paths
import argparse
from os import path
from os import listdir
# search for monitor string
import re


NITROGEN_CONFIG_FILE = "nitrogen/bg-saved.cfg"
CONFIG_FILE = "nitrogen-rotation.yaml"

DEFAULT_ALL_MONITORS = "all"


def try_parse_config_file(filename):
    try:
        with open(filename, 'r') as stream:
            return yaml.load(stream)
    except yaml.YAMLError:
        return None
    except FileNotFoundError:
        return None


def create_configuration(wallpaper_path):
    # read all files
    files = [f for f in listdir(wallpaper_path) if path.isfile(path.join(wallpaper_path, f))]
    # keep all files ending in .png and .jpg
    files = [f for f in files if f.endswith(".png") or f.endswith(".jpg")]
    # create dict
    conf = dict(wallpaper_path=wallpaper_path,
                wallpapers=files,
                monitor=DEFAULT_ALL_MONITORS)
    return conf


def write_configuration(conf, filename):
    with open(filename, 'w') as outfile:
        outfile.write(yaml.dump(conf, default_flow_style=False))


def is_valid_folder(parser, arg):
    expanded = path.expanduser(arg)
    if not path.isdir(expanded):
        parser.error("The wallpaper path %s is invalid." % expanded)
    else:
        return expanded


def rewrite_nitrogen_configuration(nitrogen_config_file, conf):

    try:
        with open(nitrogen_config_file) as f:
            lines = f.readlines()

        # search for monitor line
        if not conf['monitor'] or conf['monitor'] == DEFAULT_ALL_MONITORS:
            p = re.compile(r'\[.+\]\n')
            monitor_lines = [i for i, x in enumerate(lines) if p.match(x)]

        else:
            search_string = "[" + conf['monitor'] + "]\n"
            monitor_lines = [i for i, x in enumerate(lines) if x == search_string]

        if not monitor_lines:
            print("No matching monitor in nitrogen configuration found!.")
            return None

        wallpaper_not_found = False
        for monitor in monitor_lines:
            # search for 'file=' in monitor description block
            for l_index in range(monitor, monitor + 3):
                if lines[l_index].startswith('file='):
                    break
            else:
                continue

            # separate filename from rest of path
            pos = lines[l_index].rfind('/')
            if pos == -1:
                return None

            current = lines[l_index][pos+1:-1]
            wallpapers = conf['wallpapers']
            full_path = ""

            # search for wallpaper in list, remember index
            current_index = 0
            for index, pic in enumerate(wallpapers):
                if pic == current:
                    current_index = (index + 1) % len(wallpapers)
                    break

            # search for existing wallpaper
            while True:
                # no wallpaper is existing on disk
                if not wallpapers:
                    return False

                # next index (no need for ++ because of del operation at loop end
                current_index %= len(wallpapers)

                # re-write line
                full_path = path.join(conf['wallpaper_path'], wallpapers[current_index])
                if path.isfile(full_path):
                    break

                del wallpapers[current_index]
                wallpaper_not_found = True

            lines[l_index] = "file=" + full_path + '\n'

        # write back into file
        with open(nitrogen_config_file, 'w') as output:
            output.writelines(lines)

        # return False if a wallpaper could not be found
        return not wallpaper_not_found

    except IOError:
        return None


def main():

    config_path = path.join(path.expanduser("~"), ".config")
    config_file = path.join(config_path, CONFIG_FILE)
    configuration = try_parse_config_file(config_file)
    initial_config = configuration
    arg_required = True if not configuration else False
    configuration_changed = False

    if arg_required:
        print("No Configuration found. Parsing arguments.")

    parser = argparse.ArgumentParser(description="Rotate wallpaper (x-window root) using nitrogen.")
    parser.add_argument('--wallpaper-path', dest="path", required=arg_required, metavar="PATH",
                        type=lambda x: is_valid_folder(parser, x), help="Wallpaper location")
    parser.add_argument('--monitor', dest="monitor", required=False, metavar="MONITOR",
                        help="Monitor to set wallpaper, see nitrogen config file.")
    parser.add_argument('--rewrite', action='store_true', dest='rewrite',
                        help='Force re-scanning wallpaper dir and writing a new configuration file')
    args = parser.parse_args()

    # need a new configuration?
    if args.rewrite or args.monitor or args.path:
        if args.path:
            configuration = create_configuration(args.path)
        elif args.rewrite:
            configuration = create_configuration(configuration['wallpaper_path'])
        if args.monitor:
            configuration['monitor'] = args.monitor
        elif initial_config:
            configuration['monitor'] = initial_config['monitor']

        configuration_changed = True

    # write next wallpaper to nitrogen configuration
    ret = rewrite_nitrogen_configuration(path.join(config_path, NITROGEN_CONFIG_FILE), configuration)
    # Only if ret is False: rewrite configuration omitting removed wallpapers
    if ret is not None and not ret:
        configuration_changed = True

    # update own configuration
    if configuration_changed:
        write_configuration(configuration, config_file)


if __name__ == "__main__":
    main()
