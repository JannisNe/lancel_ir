from pathlib import Path
from timewise_sup.config_loader import TimewiseSUPConfigLoader
from timewise_sup.meta_analysis.baseline_subtraction import get_single_lightcurve


def get_lancel_ir_lightcurves():

    this_dir = Path(__file__).parent
    config_file = this_dir / "analysis.yaml"
    config = TimewiseSUPConfigLoader.read_yaml(config_file).parse_config()

    return get_single_lightcurve(
        base_name=config.wise_data.base_name,
        database_name=config.database_name,
        wise_data=config.wise_data,
        index=0,
        service="gator"
    )