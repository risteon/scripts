#!/usr/bin/env python3

NITROGEN_CONFIG_PATH = "/home/christoph/.config/nitrogen/bg-saved.cfg"
BACKGROUND_PATH = "/home/christoph/ownCloud/pictures/backgrounds"
BACKGROUND_PICTURES = [
    "aston_martin_21_9.jpg",
    "dark_road_21_9.jpg",
    "grand_canyon_21_9.jpg",
    "new_york_21_9.jpg",
    "bridge.jpg",
    "miniature_rocket_21_9.jpg",
    "ngppS8Z_21_9.jpg",
    "rotating_stars_21_9.jpg",
    "seattle_21_9.jpg",
    "sunset_over_rocks_21_9.jpg",
    "green_forest_21_9.jpg"
]


def main():

    try:
        with open(NITROGEN_CONFIG_PATH) as f:
            lines = f.readlines()

        # search for monitor: '[xin_2]'
        monitor_line = [i for i, x in enumerate(lines) if x == '[xin_2]\n']
        if not monitor_line:
            return -1

        # search for 'file=' in monitor description block
        for l_index in range(monitor_line[0], monitor_line[0] + 3):
            if lines[l_index].startswith('file='):
                break
        else:
            return -1

        pos = lines[l_index].rfind('/')
        if pos == -1:
            return -1
        if lines[l_index][5:pos] != BACKGROUND_PATH:
            return -1

        current = lines[l_index][pos+1:-1]
        for index, pic in enumerate(BACKGROUND_PICTURES):
            if pic == current:
                new = BACKGROUND_PICTURES[(index + 1) % len(BACKGROUND_PICTURES)]
                break
        else:
            new = BACKGROUND_PICTURES[0]

        # re-write line
        lines[l_index] = lines[l_index][:pos+1] + new + '\n'

        # write back into file
        with open(NITROGEN_CONFIG_PATH, 'w') as output:
            output.writelines(lines)

    except IOError:
        return -1

if __name__ == "__main__":
    main()
