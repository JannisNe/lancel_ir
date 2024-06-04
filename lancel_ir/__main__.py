import logging
from lancel_ir import plot_lightcurve, sky_plot, lightcurve_analysis


if __name__ == '__main__':
    logging.getLogger("timewise").setLevel("INFO")
    logging.getLogger("lancel_ir").setLevel("INFO")
    plot_lightcurve()
    sky_plot()
    lightcurve_analysis()
