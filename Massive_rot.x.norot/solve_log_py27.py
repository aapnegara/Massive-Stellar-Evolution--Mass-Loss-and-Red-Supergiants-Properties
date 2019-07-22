import string
from os.path import join

import numpy as np
import matplotlib.pyplot as plt

def num_columns_rows(size_file):
    '''Reads size file in returns number of columns and rows in a tuple.'''
    f = open(size_file)
    data = string.split(f.read())
    f.close()
    return (int(data[0]), int(data[1]))

def format_data(data_file, num_cols, num_rows):
    '''Reads data from file and reshapes it to be an nxm array.'''
    data = np.genfromtxt(data_file)
    return data.reshape((num_rows, num_cols))

def plot_data(data_file, num_cols, num_rows, min_zone=1, max_zone=None,
    title=None):
    '''Makes and returns a plot of data from a hydro dump.

    PARAMETERS
    ----------
    data_file : str
        path to file from which to plot
    num_cols : int
        number of columns that data should have (should get from 
        `num_columns_rows`)
    num_rows : int
        number of rows that data should have (should get from
        `num_columns_rows`)
    min_zone : int, optional
        outermost zone to be plotted (default is 1 for surface)
    max_zone : int, optional
        innermost zone to be plotted (default is None meaning innermost cell)

    RETURNS
    -------
    matplotlib figure
    '''
    if max_zone is None:
        max_zone = num_cols
    data = format_data(data_file, num_cols, num_rows)
    minmax = max([-min(data.flatten()), max(data.flatten())])
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(111)
    if title is not None:
        ax.set_title(title)
    im = ax.imshow(data, aspect='auto', cmap='RdBu',
        origin='lower', extent=(1, num_cols, 0, num_rows), vmin=-minmax,
        vmax=minmax)
    ax.set_xlabel('Zone')
    ax.set_ylabel('Iteration')
    ax.set_xlim(max_zone, min_zone)
    fig.colorbar(im)
    return fig

def make_iter_plot(name, dir=join('.', 'plot_data', 'solve_logs'), 
    min_zone=1, max_zone=None):
    '''Wrapper for easy use of `plot_data`.

    PARAMETERS
    ----------
    name : str
        name of parameter to plot (found in names.data)
    dir : str, optional
        path to data files from hydro dump. Default is ./plot_data/solve_logs,
        which should work from a properly setup work directory
    min_zone : int, optional
        outermost zone to be plotted (default is 1 for surface)
    max_zone : int, optional
        innermost zone to be plotted (default is None meaning innermost cell)

    RETURNS
    -------
    matplotlib figure
    '''
    data_file = join(dir, "{}.log".format(name))
    size_file = join(dir, 'size.data')
    num_cols, num_rows = num_columns_rows(size_file)
    return plot_data(data_file, num_cols, num_rows, min_zone=min_zone,
        max_zone=max_zone, title=name.replace('_', ' '))


if __name__ == '__main__':
    fig = make_iter_plot('corr_lnd', min_zone = 1, max_zone = None)
    fig.savefig('corr_lnd.pdf')
