FROM python:3.11

RUN apt-get update && apt-get install -yq \
    curl git vim tmux \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /reflow

COPY . .
RUN pip install -r requirements.txt

CMD ["/bin/bash"]