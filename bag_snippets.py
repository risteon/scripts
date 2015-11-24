#!/usr/bin/env python3

from collections import namedtuple
import rosbag
from rospy import rostime
from os import listdir
from os import path
from os import makedirs

FOLDERNAME_PREFIX = "snippet_"

Marker = namedtuple("Marker", ["walltime"])
SnippetDef = namedtuple("SnippetDef", ["begin", "end", "rosbag"])


def get_bagfiles(bag_path):
    bagfiles = []
    for bag_file in listdir(bag_path):
        if bag_file.endswith(".bag"):
            bagfiles.append(bag_path + "/" + bag_file)



    return bagfiles


def make_snippets(bagfiles, target_path, markers, time_before, time_after):

    previous_walltime = 0
    snippets = []
    for marker in markers:
        if marker.walltime == previous_walltime:
            continue
        previous_walltime = marker.walltime
        walltime_begin = marker.walltime - time_before
        walltime_end = marker.walltime + time_after

        foldername = target_path + "/" + FOLDERNAME_PREFIX \
                     + str(walltime_begin) + "_" + str(walltime_end)

        if not path.exists(foldername):
            makedirs(foldername)

        snippets.append(SnippetDef(rosbag=rosbag.Bag(foldername + "/snippet.bag", 'w'),
                                   begin=rostime.Time(secs=walltime_begin, nsecs=0),
                                   end=rostime.Time(secs=walltime_end, nsecs=0)))

    for bagfile in bagfiles:
        try:
            input_bag = rosbag.Bag(bagfile, 'r')
        except IOError:
            continue
        for topic, msg, t in input_bag.read_messages():
            for snip in snippets:
                if snip.begin <= t <= snip.end:
                    snip.rosbag.write(topic, msg, t)

    for snip in snippets:
        snip.rosbag.close()


def main():

    bagfiles = get_bagfiles("/home/christoph/bagfiles/2016-03-14_18-56-07")
    markers = [Marker(walltime=1457978178)]
    markers.append(Marker(walltime=1457978175))
    make_snippets(bagfiles, "/home/christoph/bagfiles/2016-03-14_18-56-07", markers, 10, 10)

if __name__ == "__main__":
    main()
