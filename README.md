# System Monitor and Overview
 
Started as a tiny script for monitoring multiple servers.  
Currently, cpu usage, gpu and memory amount will be collected and displayed.  
We use it in our lab to monitor the workload of our machine learning servers.

## Server Preview

![Sysmon preview](img/preview.png)

## Features

There are two modules that work in tandem.  
The first is sysmon_client, which can collect usage statistics and sends them to a 
running server instance.  
The second in sysmon_server, which is a Flask application that receives the usage data 
and shows a webpage with graphs.
You can also use the sysmon_client to specify tasks to run on multiply remotes machines 
in parallel. There are some limitation to that, as all machines need a relatively similar
setup and for the most part only single python script execution is supported.

## Planned features

While out of time for this internship:  
Noteworthy enhancements need to be made in particular to the handling of settings.
Most things can only be declared for one whole task, not for each remote machine separately.
Next to this there are a few enhancements for the style and information shown 
at the webpage planned.  
Some documentation. Mainly about the client, since you can and will need to import it 
and tell it what to do. Most functions already have docstrings, tho.

## Distribution

The plan is to have both, client and server, available via `pip install`.  
While currently not maintained since we are changing a lot in the early stages, you can 
later clone and build docker images of sysmon. Please note that for gpu statistics in 
Docker the gpu must be accessible by Docker and the running container.
