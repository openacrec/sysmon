import unittest

import hydra
from omegaconf import OmegaConf
# import sysmon_client.client as client


class TestFoundConfig(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_with_initialize(self):
        orig = OmegaConf.load("../src/sysmon_client/config/config.yaml")
        with hydra.initialize(config_path="../src/sysmon_client/config"):
            # config is relative to a module
            cfg = hydra.compose(config_name="config")
            self.assertEqual(cfg, orig)

    # This test manually start the map. Since it is designed to continue
    # operation, this test can't be used with automated tests
    # def test_config_found(self):
    #     try:
    #         client.start_reporting()
    #     except hydra.MissingConfigException:
    #         self.fail("Config file was not found.")


if __name__ == '__main__':
    unittest.main()
