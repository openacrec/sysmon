# System Monitor Client

Started from [sysmon](https://github.com/raphaelmemmesheimer/sysmon).  
A tiny library for monitoring multiple servers.  
Collect CPU, Memory and GPU usage and submit it to a sysmon-server instance.  
We use it in our lab to monitor the workload of our machine learning servers.

## Usage

Use from your own script by importing sysmon_client:

```python
from sysmon_client.client import Client

Client("Test", "http://server_adress:5000").start_reporting()
```

or call the pip script

```shell
sysmon-report
```

or run the Dockerfile in interactive mode (-it):

```shell
cd sysmon-docker/sysmon-client
docker build -t sysmon .
docker run -it --name sysmon sysmon
```

For more information about the projects plans and direction look at the main [Readme](../README.md).