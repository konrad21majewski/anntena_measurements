# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


def dbm_to_mw(dbm):
    """Converts a value in dBm to mW."""
    return 10 ** (dbm / 10)


def standardize_1(lst):
    max_val = max(lst)
    min_val = min(lst)
    if max_val == min_val:
        return [0.5] * len(lst)  # if all values are the same, return a list of 0.5s
    else:
        return [(x - min_val) / (max_val - min_val) for x in lst]


def standardize_neg30_to_0(lst):
    max_val = max(lst)
    min_val = min(lst)
    if max_val == min_val:
        return [0] * len(lst)  # if all values are the same, return a list of 0s
    else:
        return [((x - max_val) / (min_val - max_val)) * (-30) for x in lst]


def standardize_180(lst):
    max_val = max(lst)
    min_val = min(lst)
    if max_val == min_val:
        return [0] * len(lst)  # if all values are the same, return a list of 0s
    else:
        return [(2 * (x - min_val) / (max_val - min_val) - 1) * 180 for x in lst]


# returns a list of lists x and y containg chosen data from (int) fromhere sample to (int) tohere sample.
def txt_to_axislists(file_name, fromx, tox):
    x = []
    y = []
    with open(file_name) as my_file:
        for row in my_file:
            if row[0].isdigit():
                lines = [i for i in row.split(";")]
                data_x = float(lines[0].replace(',', '.'))
                data_y = float(lines[1].replace(',', '.'))
                if fromx < data_x < tox:
                    x.append(data_x)
                    y.append(data_y)
    return x, y




def graph(axislists, xlabel, ylabel, ifNotDB, title):
    x = axislists[0]
    y = axislists[1]


    # standarization of data
    if ifNotDB:
        y = [dbm_to_mw(i) for i in y]  # converts elements of x list to mW
        y = standardize_1(y)

    if not ifNotDB:
        y = standardize_1(y)
        y = standardize_neg30_to_0(y)

    x = standardize_180(x)


    plt.plot(x, y, c='g')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(visible=True)
    plt.title(title)
    plt.show()


def graph_polar(axislist, ifNotDB, title):
    x = np.radians(axislist[0])
    y = axislist[1]

    if ifNotDB:
        y = [dbm_to_mw(i) for i in y]  # converts elements of x list to mW
        y = standardize_1(y)

    if not ifNotDB:
        y = standardize_1(y)
        y = standardize_neg30_to_0(y)

    x = standardize_180(x)
    x = np.radians(x)

    # Plot the data in polar coordinates
    ax = plt.subplot(111, projection='polar')

    ax.plot(x, y)
    ax.set_rmax(max(y))  # Set the radial limit for the plot
    ax.set_theta_zero_location("N")  # Set the origin of the plot to the North
    ax.set_theta_direction(-1)  # Set the direction of the plot to clockwise
    plt.title(title)

    # Show the plot
    plt.show()


if __name__ == '__main__':
    # 7-71, because in the rest of measurement antenna is not moving
    data_E = txt_to_axislists('anntena_measurements/LAB2_E.TXT', 7, 71)
    graph(data_E, 'kąt [°]', 'moc', True, 'Zależność mocy od kąta')
    graph_polar(data_E, True, "Zależność mocy od kąta")

    data_H = txt_to_axislists('anntena_measurements/LAB2_H.TXT', 7, 71)
    graph(data_H, 'kąt [°]', 'moc', True, 'Zależność mocy od kąta')
    graph_polar(data_H, True, "Zależność mocy od kąta")

