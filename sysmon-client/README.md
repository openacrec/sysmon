# System Monitor Client

Fork of [sysmon](https://github.com/raphaelmemmesheimer/sysmon).  
A tiny library for monitoring multiple servers.  
Collect CPU, Memory and GPU usage and submit it to a sysmon-server instance.  
We use it in our lab to monitor the workload of our machine learning servers.

## Preview of the server

![Sysmon preview](../img/preview.png)

## Usage

Use from your own script by importing:

```python
import sysmon_client.client as client

client.start_reporting("Test", "http://server_adress:5000")
```

Planned features:

* Schedule tasks across multiple servers
  * copy necessary files over
  * start your script from sysmon_client
  * see status on the servers page  