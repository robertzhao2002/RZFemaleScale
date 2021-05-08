import numpy as np
import triangle_utils as tri
import csv
import random

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def example_data():
    raw_data = []
    data = [['BAD', 'CUTE', 'HOT']]
    file = open("CHICKS.csv")
    reader = csv.reader(file, delimiter=',')
    num_lines= len(list(reader))

    #Reset buffer
    file = open("CHICKS.csv")
    reader = csv.reader(file, delimiter=',')
    rows_to_display = list(range(num_lines))
    random.shuffle(rows_to_display)
    rows_to_display = rows_to_display[0:4]
    reader_list = list(reader)
    for i in rows_to_display:
        raw_data.append(reader_list[i])
    for j in raw_data:
        to_add = (j[0], [[float(j[1]), float(j[2]), float(j[3])]])
        data.append(to_add)
    return data

if __name__ == '__main__':
    N = 3
    theta = radar_factory(N, frame='circle')

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