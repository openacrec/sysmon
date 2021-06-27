FROM ubuntu:20.04

RUN adduser --disabled-password --gecos '' ami

# Install Python
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.9 python3-pip python3.9-dev

WORKDIR /home/ami
EXPOSE 5000

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/sysmon_server/app.py .
COPY src/sysmon_server/static/chart.js static/chart.js
COPY src/sysmon_server/templates templates/

RUN chown ami:ami -R /home/ami/
USER ami

CMD ["flask", "run", "--host=0.0.0.0"]