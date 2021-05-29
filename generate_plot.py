import numpy as np
import triangle_utils as tri
import csv
import random
import radar_utils as RU

import matplotlib.pyplot as plt

def example_data():
    raw_data = []
    data = [['BAD', 'CUTE', 'HOT']]
    file = open("CHICKS.csv")
    reader = csv.reader(file, delimiter=',')
    reader_list = list(reader)[1:]
    print(reader_list)
    num_lines= len(reader_list)

    rows_to_display = list(range(num_lines))
    random.shuffle(rows_to_display)
    rows_to_display = rows_to_display[0:4]
    
    for i in rows_to_display:
        raw_data.append(reader_list[i])
    for j in raw_data:
        to_add = (j[0], [[float(j[1]), float(j[2]), float(j[3])]])
        data.append(to_add)
    return data

if __name__ == '__main__':
    N = 3
    theta = RU.radar_factory(N, frame='circle')

    data = example_data()
    spoke_labels = data.pop(0)

    for i in range(0, len(data)):
        list_temp = list(data[i])
        side_a = tri.sideLength(data[i][1][0][0], data[i][1][0][1])
        side_b = tri.sideLength(data[i][1][0][2], data[i][1][0][1])
        side_c = tri.sideLength(data[i][1][0][0], data[i][1][0][2])
        area = round(tri.triArea(side_a, side_b, side_c), 3)
        list_temp[0]=str(data[i][0]) + ' [B, C, H]: ' + str(data[i][1][0]) + '\nArea: ' + str(area) + ', PERFECT: ' + str(round(tri.PERFECT_AREA, 3))
        data[i]=tuple(list_temp)

    fig, axs = plt.subplots(figsize=(9, 9), nrows=2, ncols=2,
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['b']
    # Plot the four cases from the example data on separate axes
    for ax, (title, case_data) in zip(axs.flat, data):
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        for d, color in zip(case_data, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
            ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1])
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot

    fig.text(0.5, 0.965, 'The BAD-CUTE-HOT (BCH) Female Scale',
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()