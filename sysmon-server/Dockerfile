FROM ubuntu:20.04

# Install Python
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.9 python3-pip python3.9-dev

WORKDIR /usr/src/app
EXPOSE 5000

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py .
COPY static static/
COPY templates templates/

#RUN adduser --disabled-password --gecos '' ami
#USER ami

CMD [ "flask", "run", "--host=0.0.0.0"]