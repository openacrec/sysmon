import unittest

import hydra
from omegaconf import OmegaConf
import sysmon_client.main as main


class TestFoundConfig(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_with_initialize(self):
        orig = OmegaConf.load("../src/sysmon_client/config/config.yaml")
        with hydra.initialize(config_path="../src/sysmon_client/config"):
            # config is relative to a module
            cfg = hydra.compose(config_name="config")
            self.assertEqual(cfg, orig)

    # def test_config_found(self):
    #     try:
    #         main.sysmon_app()
    #     except hydra.MissingConfigException:
    #         self.fail("Config file was not found.")


if __name__ == '__main__':
    unittest.main()
