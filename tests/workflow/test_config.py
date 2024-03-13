import os.path

from quant_factorizer.workflow.config import load_config


def test_load_config_file():
    with open(os.path.join('fixture', 'workflow.toml'), 'r') as f:
        conf = load_config(f)
        print(conf)
