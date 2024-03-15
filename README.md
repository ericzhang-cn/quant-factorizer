<h1 align="center" id="title">Quant Factorizer</h1>

<p align="center"><img src="https://socialify.git.ci/ericzhang-cn/quant-factorizer/image?description=1&amp;font=Inter&amp;language=1&amp;name=1&amp;pattern=Solid&amp;theme=Light" alt="project-image"></p>

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

<h2>💡 Features</h2>

Here're some of the project's best features:

- Calculate evaluate and visualize quantitative factors in one pass
- Supports single-factor and cross-factor calculations
- Built-in common factors and cross methods
- Could extend your own factor calculation factor crossover and factor evaluation methods

<h2>⚡ Get Started</h2>
<h3>Prerequisites</h3>

- [Python](https://www.python.org/) (>=3.9)
- [Poetry](https://python-poetry.org/)
- [TA-Lib](https://ta-lib.org/)

<h3>Steps</h3>
<p>1. Clone the repo</p>

```sh
git clone https://github.com/ericzhang-cn/quant-factorizer.git
cd quant-factorizer
```

<p>2. Create virtualenv</p>

```sh
poetry env use /path/to/your/python/interpreter
```

<p>3. Install dependencies</p>

```sh
poetry install
```

<p>4. Run example workflow</p>

```sh
poetry run qf run --workflow fixture/workflow.toml
```

or

```sh
poetry shell
qf run --workflow fixture/workflow.toml
```

You will find the result file: `fixture/indicators.csv`.

<h2>📖 User Guide</h2>

<h3>Command-line Interface</h3>

<h4>Run Workflow (run)</h4>

The `run` command runs the workflow defined in the workflow file.

```text
Usage: qf run [OPTIONS]

  Runs a workflow.

Options:
  --workflow FILENAME          Workflow configuration file.  [required]
  --begin ARROW                Begin time (included).
  --end ARROW                  End time (excluded).
  --concurrency INTEGER RANGE  The number of concurrent processes to use.
                               [x>=1]
  --help                       Show this message and exit.
```

| Option        | Description                                                                 | Type   | Remarks |
|---------------|-----------------------------------------------------------------------------|--------|---------|
| --workflow    | The workflow configuration file path.                                       | String |         |
| --begin       | The begin time. Such as `2023-01-01 00:00:00`. This time point is included. | Arrow  |         |
| --end         | The end time. Such as `2024-01-01 00:00:00`. This time point is excluded.   | Arrow  |         |
| --concurrency | The number of concurrent processes to use. Default is 1.                    | Arrow  |         |

<h3>Write Workflow</h3>

<h4>Overview</h4>

Quant Factorizer use [TOML (Tom's Obvious, Minimal Language)](https://toml.io/en/) as workflow configuration format.

The workflow configuration file defines the steps and parameters for a specific data processing workflow. In the context
of our project, it outlines how data should be loaded, transformed, and written back.

<h4>Structure</h4>

The configuration file consists of several sections, each dedicated to a different aspect of the workflow:

1. **name**: Specifies the name of the workflow, which can be used for identification and logging purposes.

2. **data**: Contains settings related to data loading and writing.
    - **loader**: Defines the type of data loader to use (e.g., CSV) and its associated arguments (such as the file path
      and time field).
    - **writer**: Specifies the type of data writer (e.g., CSV) and its configuration (like the output file path).
3. **factor**: Describes the calculation and application of various factors or indicators to the loaded data.\
    - **indicators**: Lists the indicators to be computed, along with their respective arguments (like periods for
      moving averages).
    - **crosses**: Defines cross-computations or transformations to be applied to the indicators, including their order
      and any additional arguments.

<h4>Editing Instructions</h4>

When editing the configuration file:

1. Ensure that you follow the TOML syntax correctly. TOML is sensitive to indentation and formatting.
2. Modify the existing sections or add new ones as needed for your workflow. For example, you might add more indicators
   or change the data loader arguments.
3. Provide valid values for all required fields. Refer to the documentation or existing examples for guidance on
   acceptable values and formats.
4. If adding new indicators or cross-computations, ensure that their names and arguments are supported by the underlying
   library or framework.
5. Save the file with a .toml extension in the appropriate directory for your project.

<h4>Example</h4>

The following is an example of a valid TOML workflow configuration file:

```toml
name = "Demo Workflow"

[data]
[data.loader]
name = "csv"
[data.loader.args]
file_path = "fixture/ohlcv_example.csv"
time_field = "candle_begin_time"

[data.writer]
name = "csv"
[data.writer.args]
file_path = "fixture/indicators.csv"

[factor]
[[factor.indicators]]
name = "SMA"
args = { periods = [6, 24, 48] }
[[factor.indicators]]
name = "RSI"
args = { periods = [12, 24] }
[[factor.indicators]]
name = "ATR"
args = { periods = [12, 24] }

[[factor.crosses]]
name = "MUL"
orders = [2]
args = { }
[[factor.crosses]]
name = "PCA"
orders = [-1]
args = { n_components = 3 }
[[factor.crosses]]
name = "W_SUM"
orders = [2]
args = { weights = [[0.5, 0.5]] }
```

<h3>Built-in Loaders</h3>

<h4>CSVLoader</h4>

CSVLoader is a data loader that reads data from a CSV file.

<h5>name</h5>
csv

<h5>Arguments</h5>

| Argument     | Description                                         | Type   | Remarks  |
|--------------|-----------------------------------------------------|--------|----------|
| file_path    | The path to the CSV file containing the OHLCV data. | String | Required |
| time_field   | The name of the column containing the time series.  | String | Optional |
| symbol_field | The name of the column containing the asset symbol. | String | Optional |
| open_field   | The name of the column containing the open value.   | String | Optional |
| close_field  | The name of the column containing the close value.  | String | Optional |
| high_field   | The name of the column containing the high value.   | String | Optional |
| low_field    | The name of the column containing the low value.    | String | Optional |
| volume_field | The name of the column containing the volume value. | String | Optional |

<h4>PickleLoader</h4>

PickleLoader is a data loader that reads data from a pickle file.

<h5>name</h5>
pickle

<h5>Arguments</h5>

| Argument     | Description                                            | Type   | Remarks  |
|--------------|--------------------------------------------------------|--------|----------|
| file_path    | The path to the pickle file containing the OHLCV data. | String | Required |
| time_field   | The name of the column containing the time series.     | String | Optional |
| symbol_field | The name of the column containing the asset symbol.    | String | Optional |
| open_field   | The name of the column containing the open value.      | String | Optional |
| close_field  | The name of the column containing the close value.     | String | Optional |
| high_field   | The name of the column containing the high value.      | String | Optional |
| low_field    | The name of the column containing the low value.       | String | Optional |
| volume_field | The name of the column containing the volume value.    | String | Optional |

<h3>Built-in Writers</h3>

<h4>CSVWriter</h4>

CSVWriter is a data writer that writes data to a CSV file.

<h5>name</h5>
csv

<h5>Arguments</h5>

| Argument  | Description                                       | Type   | Remarks  |
|-----------|---------------------------------------------------|--------|----------|
| file_path | The path to the CSV file to write the OHLCV data. | String | Required |

<h4>PickleWriter</h4>

PickleWriter is a data writer that writes data to a pickle file.

<h5>name</h5>
pickle

<h5>Arguments</h5>

| Argument  | Description                                          | Type   | Remarks  |
|-----------|------------------------------------------------------|--------|----------|
| file_path | The path to the pickle file to write the OHLCV data. | String | Required |

<h3>Built-in Indicators</h3>

| Name                 | Description                                                                                                | Arguments                                                        | Remarks |
|----------------------|------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|---------|
| SMA                  | The Simple Moving Average calculates the average price of an asset over a specified number of periods.     | periods                                                          |         |
| RSI                  | The Relative Strength Index (RSI) is a momentum indicator that measures the strength of a security's price | periods                                                          |         |
| Return               | The gain or loss generated on an investment over a specific period of time.                                | periods                                                          |         |
| Percentage_Of_Return | The rate of return.                                                                                        | periods                                                          |         |
| OBV                  | On-Balance Volume.                                                                                         |                                                                  |         |
| AD                   | Accumulation/Distribution Line.                                                                            |                                                                  |         |
| ADX                  | Average Directional Index.                                                                                 | periods                                                          |         |
| Aroon                | Aroon Indicator.                                                                                           | periods                                                          |         |
| MACD                 | Moving Average Convergence Divergence.                                                                     | fast_period/slow_period/signal_period                            |         |
| STOCH                | Stochastic Oscillator.                                                                                     | fastk_period/slowk_period/slowk_matype/slowd_period/slowd_matype |         |
| ATR                  | Average True Range.                                                                                        | periods                                                          |         |
| BIAS                 | The percentage deviation of the closing price from the moving average.                                     | periods                                                          |         |
| PRR                  | Price Range Ratio.                                                                                         |                                                                  |         |
| ROC                  | Rate of Change.                                                                                            | periods                                                          |         |
| AMP                  | Amplitude.                                                                                                 | periods                                                          |         |
| VOL                  | Volatility.                                                                                                | periods                                                          |         |
| HL                   | High to Low.                                                                                               | periods                                                          |         |
| DPO                  | Detrended Price Oscillator.                                                                                | periods                                                          |         |

<h3>Built-in Crosses</h3>

| Name  | Description                                 | Arguments    | Remarks               |
|-------|---------------------------------------------|--------------|-----------------------|
| MUL   | Multiplication of indicators.               |              |                       |
| PCA   | Principal Component Analysis of indicators. | n_components | Orders not available. |
| W_SUM | Weighted Sum of indicators.                 | weights      |                       |

<h2>🛠 Developer Guide</h2>

<h3>Develop your own Loader or Writer</h3>

This guide outlines the steps necessary to develop custom loaders and writers for the OHLCV (Open, High, Low, Close,
Volume) data and technical indicator data, respectively. By following this guide, users can extend the functionality of
the existing data loading and writing mechanisms to support additional data sources or storage formats.

<h4>Creating a Custom Loader</h4>

1. **Import the Necessary Modules**:
   Start by importing the required modules, including the `OHLCVDataLoader` abstract base class and any other
   dependencies.
2. **Define the Custom Loader Class**:
   Create a new class that inherits from `OHLCVDataLoader`. This class will serve as the base for your custom loader.
3. **Implement the `load` Method**:
   Override the `load` method to define the logic for loading the OHLCV data from the desired source. This method should
   return a `pandas.DataFrame` containing the loaded data.
4. **Add Any Additional Methods or Properties**:
   If necessary, you can add additional methods or properties to your custom loader class to support specific
   functionality or configuration options.
5. **Register the Custom Loader**:
   Modify the `OHLCVDataLoader.get_instance` class method to include your custom loader. Add a new condition to check
   for the name of your loader and return an instance of your custom loader class.

You may refer
to [loaders.py](https://github.com/ericzhang-cn/quant-factorizer/blob/main/quant_factorizer/data/loaders.py) as an
example.

<h4>Creating a Custom Writer</h4>

1. **Import the Necessary Modules**:
   Start by importing the required modules, including the `IndicatorWriter` abstract base class and any other
   dependencies.
2. **Define the Custom Writer Class**:
   Create a new class that inherits from `IndicatorWriter`. This class will serve as the base for your custom writer.
3. **Implement the `write` Method**:
   Override the `write` method to define the logic for writing the technical indicator data to the desired destination.
   This method should take a `pandas.DataFrame` as input and write it to the specified format or storage medium.
4. **Add Any Additional Methods or Properties**:
   If necessary, you can add additional methods or properties to your custom writer class to support specific
   functionality or configuration options.
5. **Register the Custom Writer**:
   Modify the `IndicatorWriter.get_instance` class method to include your custom writer. Add a new condition to check
   for the name of your writer and return an instance of your custom writer class.

You may refer
to [writers.py](https://github.com/ericzhang-cn/quant-factorizer/blob/main/quant_factorizer/data/writers.py) as an
example.

<h3>Develop your own Indicator</h3>

To develop a custom indicator, you need to follow these steps:

1. Import the necessary libraries and modules.
2. Define your indicator function.
3. Decorate your indicator function with the `@indicator` decorator, providing a unique name and a definition for your
   indicator.
4. Register your indicator by calling the decorator function.
5. Implement the logic to calculate your indicator using the input data and periods.
6. Return the calculated indicator values as a `pd.DataFrame`.

You may refer
to [indicators.py](https://github.com/ericzhang-cn/quant-factorizer/blob/main/quant_factorizer/factor/indicators.py) as
an
example.

<h3>Develop your own Cross</h3>

To get started with indicator crossing in your project, follow these steps:

1. Import the necessary modules.
2. Define your feature cross functions using the `@cross` decorator. The decorator takes care of registering the
   function
   as a feature cross operation and provides a convenient way to access it later. Note that the function should take a
   DataFrame as the first argument and return a DataFrame with the new indicator(s).
3. Apply the indicator crosses to your data. Once you have defined your feature cross functions, you can apply them to
   your data by accessing the cross_registry dictionary and calling the registered functions.

You may refer
to [crosses.py](https://github.com/ericzhang-cn/quant-factorizer/blob/main/quant_factorizer/factor/crosses.py) as an
example.

<h2>✅ Roadmap</h2>

- Core futures
    - [x] Calculate technical indicators.
    - [x] Cross technical indicators.
    - [ ] Evaluate technical indicators.
    - [ ] Visualize technical indicators.
- Data load & write
    - Local Files
        - [x] CSV
        - [x] Pickle
        - [ ] Parquet
        - [ ] Feather
    - Relational Databases
        - [ ] MySQL
        - [ ] PostgreSQL
        - [ ] SQLite
    - NoSQL Databases
        - [ ] MongoDB
        - [ ] InfluxDB
- Enhanced scaffolding capabilities for command line tool
    - [ ] Workflow management
    - [ ] Loader & Writer management
    - [ ] Indicator & Cross management
    - [ ] Evaluation management
    - [ ] Visualization management
- Maintainability & Observability
    - [ ] Logging
    - [ ] Metrics
    - [ ] Dockerize