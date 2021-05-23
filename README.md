# System Monitor (Docker)

Dockerized version of [sysmon](https://github.com/raphaelmemmesheimer/sysmon).  
A tiny script for monitoring multiple servers. Stats currently shown are cpu, gpu, memory usage.
We use it in our lab to monitor the workload of our machine learning servers.

## Preview

![Sysmon preview](img/preview.png)

## Usage

* Open compose.yaml
* Change environment variables to fit your deployment
* `docker-compose up`