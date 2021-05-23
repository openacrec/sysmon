FROM nvidia/cuda:11.2.0-base

# Install Python
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.9 python3-pip python3.9-dev


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "main.py" ]