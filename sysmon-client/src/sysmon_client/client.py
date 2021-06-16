import hydra

import collector
import submitter


@hydra.main(config_path="config", config_name="config")
def start_reporting(cfg):
    """
    Start reporting this machines system load to the server.

    :param cfg: ConfigDict. Gets passed through by @hydra decorator
    :return:
    """
    system_stats = {
        "name": cfg.client.name,
        "interval": cfg.client.update_interval_in_s,
        "time": collector.collect_time_string(),
        "timestamp": collector.collect_time(),
        "cpu": collector.collect_cpu(),
        "memory": collector.collect_memory(),
        "gpu": collector.collect_gpu_mem()
    }

    while True:
        submitter.continues_submit(system_stats, cfg.server.address)


if __name__ == "__main__":
    start_reporting()
