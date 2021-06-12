# System Monitor Server

Server collecting system statistics from [Sysmon-Client](https://gitlab.uni-koblenz.de/mmac/sysmon-docker).  
Running on flask to display our lab's servers workload to decide which one has some capacity left.

## Preview

![Sysmon preview](../img/preview.png)

## Usage

Either as standalone script:

```bash
python src/sysmon_server/app.py
```

Build and use as Docker Container:

```
docker-compose up -d
```
