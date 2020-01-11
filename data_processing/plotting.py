
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import shapefile as shp


def plot_map(filepath=''):
    assert os.path.exists(filepath), "Input file does not exist."
    sf = shp.Reader(filepath)
    plt.figure()

    i_start = 0
    i_end = 0
    for shape in sf.shapeRecords():

        for i in range(len(shape.shape.parts)):

            i_start = shape.shape.parts[i]

            if i == len(shape.shape.parts)-1:

                i_end = len(shape.shape.points)
            
            else:
                i_end = shape.shape.parts[i+1]
            
        x = [i[0] for i in shape.shape.points[i_start:i_end]]
        y = [i[1] for i in shape.shape.points[i_start:i_end]]
        plt.plot(x,y)
    plt.show()
    return

def plot_fn(data=tuple(), labels=('X','Y'), scale="linear", title="Graph"):
    '''Disclaimer: Streamlined plotting from matplotlib functions,
                    for ease of use not claiming ownership. '''
    x, y = data
    x_label, y_label = labels
    plt.plot(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.yscale(scale)
    plt.title(title)
    plt.show()
    plt.savefig(fname=title.join('.png'), format='png')
    return


def plot_fn_3d(data=tuple(), labels=('X','Y','Z'), scale="linear", title="Graph"):
    '''
        Plotting 3D-data 
    '''
    x, y, z = data

    fig = plt.figure()
    ax = fig.add_subplot(1111, projection='3d')

    x_label, y_label = labels
    plt.plot_wireframe(x,y, z)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.yscale(scale)
    plt.title(title)
    plt.show()
    plt.savefig(fname=title.join('.png'), format='png')

    return

'''
https://gis.stackexchange.com/questions/131716/plot-shapefile-with-matplotlib
'''

# def plotting_map_shapes(sf=shp.Reader("test.shp")):

#     import shapefile as shp  # Requires the pyshp package
#     import matplotlib.pyplot as plt

#     # sf = shp.Reader("test.shp")

#     plt.figure()
#     for shape in sf.shapeRecords():
#         x = [i[0] for i in shape.shape.points[:]]
#         y = [i[1] for i in shape.shape.points[:]]
#         plt.plot(x,y)
#     plt.show()
#     return

''' 
alt solution

https://gis.stackexchange.com/questions/131716/plot-shapefile-with-matplotlib/309780#309780

'''
def alt_map_plot(map_file):

    import matplotlib.pyplot as plt
    import shapefile
    import numpy as np

    this_shapefile = shapefile.Reader(map_file) # whichever file
    shape = this_shapefile.shape(i) # whichever shape
    points = np.array(shape.points)

    intervals = list(shape.parts) + [len(shape.points)]

    ax = plt.gca()
    ax.set_aspect(1)

    for (i, j) in zip(intervals[:-1], intervals[1:]):
        ax.plot(*zip(*points[i:j]))

    return

def test():
    # plot_map(filepath="/home/ghoul/Documents/GitHub/Dorian_Analysis/tweets_data/al052019_5day_059/al052019-059_5day_lin.shp")
    # plot_map(filepath="/home/ghoul/Documents/GitHub/Dorian_Analysis/tweets_data/al052019_5day_059/al052019-059_5day_pgn.shp")
    # plot_map(filepath="/home/ghoul/Documents/GitHub/Dorian_Analysis/tweets_data/al052019_5day_059/al052019-059_5day_pts.shp")
    # plot_map(filepath="/home/ghoul/Documents/GitHub/Dorian_Analysis/tweets_data/al052019_5day_059/al052019-059_ww_wwlin.shp")

    plot_map(filepath="/home/ghoul/Documents/GitHub/Dorian_Analysis/tweets_data/al052019_5day_059A/al052019-059A_5day_lin.shp")
    plot_map(filepath="/home/ghoul/Documents/GitHub/Dorian_Analysis/tweets_data/al052019_5day_059A/al052019-059A_5day_pgn.shp")
    plot_map(filepath="/home/ghoul/Documents/GitHub/Dorian_Analysis/tweets_data/al052019_5day_059A/al052019-059A_5day_pts.shp")
    plot_map(filepath="/home/ghoul/Documents/GitHub/Dorian_Analysis/tweets_data/al052019_5day_059A/al052019-059A_ww_wwlin.shp")

    return

if __name__ == "__main__":

    test()