import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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