# System Monitor Client

Fork of [sysmon](https://github.com/raphaelmemmesheimer/sysmon).  
A tiny script for monitoring multiple servers. Stats currently shown are cpu, gpu, memory usage.  
We use it in our lab to monitor the workload of our machine learning servers.

## Preview

![Sysmon preview](../img/preview.png)

## Usage

Either as standalone script:

```bash
python main.py client.name=YourServersName server.address=https://youraddress.com/incomingStatsHere
```

Use from your own module by importing:

```python
import sysmon_client
```

Build and use as Docker Container:

```
docker-compose up -d
```
