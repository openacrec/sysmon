FROM nvidia/cuda:11.2.0-base

RUN adduser --disabled-password --gecos '' ami

# Install Python
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.9 python3-pip python3.9-dev

WORKDIR /home/ami

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/sysmon_client/main.py ./
COPY config ./config

RUN chown ami:ami -R /home/ami/
USER ami

CMD ["python3", "-u", "main.py"]