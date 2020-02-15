import csvreader
import numpy as np
import matplotlib.pyplot as plt


def add_coordinates(loc, s, x, y):
    if loc.get(s) is None:
        loc[s] = [x, y, 1]
    else:
        lst = loc[s]
        loc[s] = [lst[0] + x, lst[1] + y, lst[2] + 1]
    return None


if __name__ == '__main__':
    full_events = csvreader.csv_reader_without_headers('../data/fullevents.csv')
    passing_events = csvreader.csv_reader_without_headers('../data/passingevents.csv')
