from requests import post


def send_test(machine_name, cpu_p, mem_p, gpu_p):
    post("http://localhost:5000/post", json={
        "machine_name": machine_name,
        "cpu": [
            [
                "2021-05-23 18:45:54",
                cpu_p
            ]
        ],
        "memory": [
            mem_p
        ],
        "gpu": [
            [
                {
                    "index": "0",
                    "type": "NVIDIA GeForce GTX 1660 Ti",
                    "uuid": "GPU-c7b2d3ec-8b29-796e-ed4b-2b295e80d270",
                    "mem_used": 3072,
                    "mem_total": 6144,
                    "mem_used_percent": gpu_p
                }
            ]
        ],
    })


if __name__ == "__main__":
    send_test("asraphael", 20, 30, 40)
    send_test("Matthias-PC", 25, 35, 12.5)
