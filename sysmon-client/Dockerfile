FROM nvidia/cuda:11.2.0-base

RUN adduser --disabled-password --gecos '' ami

# Install Python
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.9 python3-pip python3.9-dev

WORKDIR /home/ami

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . ./sysmon/

RUN chown ami:ami -R /home/ami/

RUN ["pip", "install", "-e", "sysmon"]
USER ami
CMD ["sysmon-report"]

