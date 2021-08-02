from requests import post


def send_test(machine_name, time, cpu_p, mem_p, gpu_p):
    """Test sending (old) formatted json to sysmon server."""
    json = {
        "machine_name": machine_name,
        "interval": 60,
        "time": [time, time, time],
        "cpu": [cpu_p, cpu_p * 2, cpu_p + 5],
        "memory": [mem_p, mem_p + 2, mem_p - 5]
    }
    if gpu_p:
        json["gpu"] = [gpu_p, gpu_p * 2, gpu_p + 7]

    post("http://127.0.0.1:5000/post", json=json)


if __name__ == "__main__":
    send_test("asraphael", "2021-05-23 18:45:54", 20, 30, 40)
    send_test("Matthias-PC", "2021-05-24 18:45:54", 25, 35, 12.5)
    send_test("NoGpu", "2021-05-24 18:45:54", 25, 35, None)
