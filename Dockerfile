FROM python:3.10-slim-buster
LABEL Name="Retro | Modern Chess"

ARG scrDir=src
COPY $scrDir requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY $scrDir/app ./app

CMD run:app