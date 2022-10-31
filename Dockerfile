FROM python:3.10

ENV PYTHONPATH=/jsonl-formatter
WORKDIR ${PYTHONPATH}

ADD \
    jsonl_formatter.py \
    Makefile \
    requirements.txt \
    ./

RUN make init

WORKDIR /mnt/pwd

ENTRYPOINT ["python", "-m", "jsonl_formatter"]
