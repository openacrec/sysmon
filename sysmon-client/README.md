# System Monitor Client

Started from [sysmon](https://github.com/raphaelmemmesheimer/sysmon).  
A tiny library for monitoring multiple servers.  
Collect CPU, Memory and GPU usage and submit it to a sysmon-server instance.  
We use it in our lab to monitor the workload of our machine learning servers.

## Usage

Use from your own script by importing sysmon_client:

```python
import sysmon_client.client as client

client.start_reporting("Test", "http://server_adress:5000")
```

For more information about the projects plans and direction look at the main [Readme](../README.md).