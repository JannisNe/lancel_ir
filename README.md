# WISE photometry for AT2019aalc

## Installation

### 1. Clone this repository:

```bash
git clone 
```

### 2. Install the package

#### Recommended: installation via `poetry`:

```bash
poetry install
```
#### Installation with `pip`

```bash
pip install .
```


## Prerequisites

You have to have a `MongoDB` running. For installation on Mac see 
[this](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/). 
`timewise-sup` will connect to the database on the default port `27017`. 
You can change this by setting the environment variable `TIMEWISE_SUP_MONGODB_PORT`.



## Usage

### 1. Customize the configuration file
The delivered configuration file `lancel_ir/analysis.yml` will download and build the WISE lightcurve,
run the Bayesian Blocks analysis and produce and plot the baseline subtracted lightcurve.
Make sure to change the path of the coordinates file to the right one depending on your system.

### 2. Download and analyse the data

```bash
timewise_sup lancel_ir/analysis.yml -l INFO
```

### 3. Load the data externally

```python
from lancel_ir import get_lancel_ir_lightcurves
lightcurve = get_lancel_ir_lightcurves()  # returns a pandas.DataFrame
print(lightcurve.columns)                 # prints the available columns
```