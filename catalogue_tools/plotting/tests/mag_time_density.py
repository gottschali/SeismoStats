import os

import numpy as np

from catalogue_tools.plotting.mag_time_density import \
    plot_magnitude_time_density


def test_mag_time_density():
    PATH_RESOURCES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'data')
    catalogue = np.genfromtxt(
        f"{PATH_RESOURCES}/test_completeness_catalogue.csv",
        delimiter=",",
        skip_header=1)

    # Sort into it's magnitudes and years
    magnitudes = catalogue[:, 0]
    years = catalogue[:, 1]

    # completeness table
    completeness_table = np.array([[2005, 3.0],
                                   [1975, 4.0],
                                   [1960, 5.0],
                                   [1900, 6.0]])

    # As we did before, let's take a look at the density of events
    magnitude_bins = np.arange(3.0, 7.1, 0.1)

    year_bins = np.arange(years.min(), years.max() + 1, 1)

    plot_magnitude_time_density(magnitudes, years,
                                mbins=magnitude_bins,
                                time_bins=year_bins,
                                completeness_table=completeness_table,
                                filename='myfile.png')
