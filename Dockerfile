FROM jupyter/minimal-notebook

ENV dryrun 0
ENV dbhost host.docker.internal
ENV dbport 27017
ENV dbusername unset
ENV dbpass unset
ENV dbname cheques

RUN pip install pymongo

WORKDIR /usr/osama

COPY src/* src/
COPY json_files data_files/
COPY run-feeder.sh .

CMD ["sh", "-c", "/usr/osama/run-feeder.sh ${dryrun} ${dbhost} ${dbport} ${dbusername} ${dbpass} ${dbname} json_files"]
