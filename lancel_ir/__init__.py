from pathlib import Path
import logging
import pandas as pd
import numpy as np
from astropy.time import Time
from timewise.config_loader import TimewiseConfigLoader


logger = logging.getLogger("lancel_ir")
logger.addHandler(logging.getLogger("timewise").handlers[0])
redshift = 0.036
pre_flare_mjd = 58500
second_flare_mjd = 60000


def get_config():
    this_dir = Path(__file__).parent
    config_file = this_dir / "analysis.yml"
    config = TimewiseConfigLoader.read_yaml(config_file).parse_config()
    return config


def plot_lightcurve():
    logger.info("Plotting light curve")
    wd = get_config().wise_data
    wd.plot_lc(0, service="gator")


def sky_plot():
    logger.info("Plotting sky plot")
    config = get_config()
    config.wise_data.plot_diagnostic_binning(ind=0, service="gator")


def get_lightcurve():
    return pd.DataFrame.from_dict(
        get_config()
        .wise_data
        .load_data_product(service="gator")
        ["0"]["timewise_lightcurve"]
    )


def lightcurve_analysis():
    logger.info("calculating pre-flare variability")
    config = get_config()
    dp = config.wise_data.load_data_product(service="gator")
    lc = pd.DataFrame.from_dict(dp["0"]["timewise_lightcurve"])
    times = Time(lc["mean_mjd"], format="mjd")

    logger.info(f"LC times: {min(times).datetime} - {max(times).datetime}")
    pre_flare_mask = lc.mean_mjd < pre_flare_mjd
    second_flare_mask = lc.mean_mjd > second_flare_mjd
    pre_flare_lc = lc[pre_flare_mask]
    flare_lc = lc[~pre_flare_mask & ~second_flare_mask]
    second_flare_mask = lc[second_flare_mask]

    for b in ["W1", "W2"]:
        k = f"{b}_mean_flux_density"
        for df, when in zip([pre_flare_lc, flare_lc, second_flare_mask], ["pre-flare", "flare", "second-flare"]):
            _var = abs(2.5 * np.log10(df[k].max() / df[k].min()))
            logger.info(f"{b} {when} variability: {_var:.2f} mag (until {pre_flare_mjd}) mjd")

    bsl = dict()
    for b in ["W1", "W2"]:
        zp = config.wise_data.magnitude_zeropoints['F_nu'][b].to('mJy').value
        bsl[f"{b}_flux_density"] = pre_flare_lc[f"{b}_mean_flux_density"].median()
        bsl[f"{b}_mag"] = -2.5 * np.log10(bsl[f"{b}_flux_density"] / zp)
        logger.info(f"{b} baseline: {bsl[f'{b}_mag']:.2f} mag")

    baseline_color = bsl["W1_mag"] - bsl["W2_mag"]
    logger.info(f"baseline W1-W2 color: {baseline_color:.2f} mag")
