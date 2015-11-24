#!/usr/bin/env python3
__author__ = "Christoph Rist"
__copyright__ = "Copyright 2015, Christoph Rist"
__license__ = "MIT"
__email__ = "dev@bitloot.de"

from os import walk
from os import symlink
from os import unlink
from os import path
from os import readlink

import sys

workspaces_path = "/home/christoph/workspaces"
symlink_path = "/home/christoph/catkin_ws"

# colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_selection(ws, dirnames):

    try:
        selection = int(ws)
    except ValueError:
        print(bcolors.FAIL + "Not valid." + bcolors.ENDC)
        return 0

    if selection is 0:
        return 0

    if not 0 < selection <= len(dirnames):
        print(bcolors.FAIL + "Not valid." + bcolors.ENDC)
        return 0

    return selection

def read_dirnames():

    f = []
    for (dirpath, dirnames, filenames) in walk(workspaces_path):
        f.extend(filenames)
        break

    return dirnames

def choose_workspace(dirnames):

    print(bcolors.OKGREEN + "Choose available workspace:" + bcolors.ENDC)
    print("(0) cancel")
    print("----------")

    counter = 1
    for dirname in dirnames:
        print(bcolors.OKBLUE + "(", counter, ") " + bcolors.ENDC, dirname, sep='')
        counter = counter + 1
    
    
    return input("Your choice: ")

    

def switch_workspace(workspace_dir_name):

    print("Switching to", bcolors.BOLD + workspace_dir_name + bcolors.ENDC, "...")
    
    src_path = workspaces_path + "/" + workspace_dir_name

    
    if path.exists(symlink_path):
        if not path.islink(symlink_path):
            print(bcolors.FAIL + "Cannot switch,", symlink_path, "exists but is not a symlink" + bcolors.ENDC)
            return

        unlink(symlink_path)

    symlink(src_path, symlink_path)

    print(bcolors.OKGREEN + "Done." + bcolors.ENDC)


def check_workspace(dirnames):
    if not (path.exists(symlink_path) and path.islink(symlink_path)):
        return len(dirnames)

    current = readlink(symlink_path)
    for i in range(len(dirnames)):
        if workspaces_path + "/" + dirnames[i] == current:
            return i

    return len(dirnames)


def do_work(argv):

    dirnames = read_dirnames()

    c = check_workspace(dirnames)
    if c is not len(dirnames):
        print("Current:", bcolors.BOLD + dirnames[c] + bcolors.ENDC)
    else:
        print("Not on any workspace.")

    if len(argv) < 2:
        ws = choose_workspace(dirnames)
    else:
        if argv[1] is 'i':
            return

        ws = argv[1]

    ws = check_selection(ws, dirnames)

    if ws is 0:
        return

    switch_workspace(dirnames[ws-1])

    

def main(argv):
    print("###############################")

    try:
        do_work(argv)

    except KeyboardInterrupt:
        print(bcolors.FAIL + "Aborting" + bcolors.ENDC)

    print("###############################")


if __name__ == "__main__":
    main(sys.argv)

