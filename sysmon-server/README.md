# System Monitor Server

Server collecting system statistics from [Sysmon-Client](https://gitlab.uni-koblenz.de/mmac/sysmon-docker).  
Running on flask to display our lab's servers workload to decide which one has some capacity left.

## Preview

![Sysmon preview](../img/preview.png)

## Usage

Either as standalone script:

```bash
python -m flask run
```

Planned features:

* Display running tasks (defined by client)
* API to return list of "somewhat" idle servers, that can be worked on