import curses


def main(stdscr):
    stdscr.nodelay(True)
    try:
        return stdscr.getkey()
    except:
        return None


def key_pressed(key):
    inp_key = curses.wrapper(main)

    while inp_key is not None:
        if key == inp_key:
            return True
        inp_key = curses.wrapper(main)
    return False
