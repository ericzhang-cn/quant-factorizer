import os

from quant_factorizer.workflow.config import load_config
from quant_factorizer.workflow.run import run_workflow


def test_run_workflow():
    with open(os.path.join('fixture', 'workflow.toml'), 'r') as f:
        conf = load_config(f)
    r = run_workflow(conf)
