# System Monitor Server

Server receiving system statistics from [sysmon-client](../sysmon-client).  
Running on flask to display our lab's servers workload to decide which one has some capacity left.

## Webpage Preview

![Sysmon preview](../img/preview.png)

## Usage

You can start the server as any other Flask application:

```bash
cd sysmon-server/src/sysmon_server
python -m flask run
```

For more information about the projects plans and direction look at the main [Readme](../README.md).