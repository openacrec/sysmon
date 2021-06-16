import hydra
import collector
import submitter


@hydra.main(config_path="config", config_name="config")
def sysmon_app(cfg):
    """

    :param cfg: Config file. Gets passed through by @hydra decorator
    :return:
    """
    system_stats = {
        "name": cfg.client.name,
        "interval": cfg.client.update_interval_in_s,
        "time": collector.collect_time(),
        "cpu": collector.collect_cpu(),
        "memory": collector.collect_memory(),
        "gpu": collector.collect_gpu_mem()
    }

    submitter.submit(system_stats, cfg.server.address)


if __name__ == "__main__":
    sysmon_app()
