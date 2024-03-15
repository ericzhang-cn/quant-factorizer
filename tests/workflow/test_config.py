import os.path

from quant_factorizer.workflow.config import load_config


def test_load_config_file():
    with open(os.path.join('fixture', 'workflow.toml'), 'r') as f:
        conf = load_config(f)

        assert conf.name == 'Demo Workflow'

        assert conf.data.loader.name == 'csv'
        assert conf.data.loader.args == {
            'file_path': 'fixture/ohlcv_example.csv',
            'time_field': 'candle_begin_time',
        }

        assert conf.data.writer.name == 'csv'
        assert conf.data.writer.args == {
            'dir_path': 'fixture/output/',
            'prefix': 'example-',
        }

        assert conf.factor.indicators[0].name == 'SMA'
        assert conf.factor.indicators[0].args == {
            'periods': [6, 24, 48],
        }
        assert conf.factor.indicators[1].name == 'RSI'
        assert conf.factor.indicators[1].args == {
            'periods': [12, 24],
        }
        assert conf.factor.indicators[2].name == 'ATR'

        assert conf.factor.crosses[0].name == 'MUL'
        assert conf.factor.crosses[0].orders == [2]
        assert conf.factor.crosses[0].args == {}
        assert conf.factor.crosses[1].name == 'PCA'
        assert conf.factor.crosses[1].orders == [-1]
        assert conf.factor.crosses[1].args == {'n_components': 3}
        assert conf.factor.crosses[2].name == 'W_SUM'
        assert conf.factor.crosses[2].orders == [2]
        assert conf.factor.crosses[2].args == {'weights': [[0.5, 0.5]]}
