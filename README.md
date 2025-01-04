# quickstart

This is a quickstart guide to get you up and running with the FHIR Aggregator.

## Installation

* setup a virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r scripts/requirements.txt
```


## dev, staging, prod

* See https://github.com/FHIR-Aggregator/cloud

## local development
* See .env-sample and setup the environment variables
* Follow the instructions in the cloud/README.md to starr and monitor the server
* Query the server to verify it is running:

```bash
 curl -s $FHIR_BASE'/metadata' > /dev/null && echo 'OK: server running'
OK: server running
```

## load the data

```bash
# set the project name, used as a prefix for the bucket objects
export PROJECT_NAME=TCGA-CHANGEME
```


* Upload your data to the public bucket. See scripts/upload.sh for details.

* Create a manifest file to describe the data you want to load. See scripts/create-manifest.py for details.

```bash
python create-bulk-import-request.py --help
Usage: create-bulk-import-request.py [OPTIONS] FULL_PATH PROJECT_NAME

  Create manifest for loading FHIR data from bucket.

  Arguments:

  full_path (str): The source of the FHIR ndjson files in the local file
  system. project_name (str): The path in the bucket.

Options:
  --input-source TEXT  The publicly available https:// url base
  --help               Show this message and exit.

```

* start a job to load from a `public` bucket


```bash
# local
unset AUTH
# deployed, change to your credentials
export AUTH='-u USER:PASS'

curl -vvvv $AUTH --header "X-Upsert-Extistence-Check: disabled" --header "Content-Type: application/fhir+json" --header "Prefer: respond-async"  -X POST $FHIR_BASE'/$import' --data @bulk-import-request-PROJECT_NAME.json 

```
*Note:*
> The first time this command is run after restarting the server, it may take a few ( well more than a few ) minutes  to respond. Subsequent runs will be faster.
> See https://groups.google.com/g/hapi-fhir/c/V87IZHvlDyM/m/JIOvBvgwAQAJ

* check the status of the job

```bash
# where XXXX came from the response of the previous command
curl $FHIR_BASE'/$import-poll-status?_jobId=XXXX'

```

* check the status of the server

Navigate to project root dir to run docker compose commands.
Use standard docker compose commands, e.g. 

* show running
```bash
docker compose ps
NAME                        IMAGE                     COMMAND                  SERVICE                     CREATED          STATUS          PORTS
hapi-fhir-jpaserver-start   hapiproject/hapi:v7.4.0   "java --class-path /…"   hapi-fhir-jpaserver-start   27 minutes ago   Up 27 minutes   0.0.0.0:8080->8080/tcp
hapi-fhir-postgres          postgres:15-alpine        "docker-entrypoint.s…"   hapi-fhir-postgres          27 minutes ago   Up 27 minutes   5432/tcp
```

* show logs
```bash
# show the last 10 lines of the logs and wait for more ...
docker compose logs --tail 10 -f
```

* show service utilization
```bash
docker compose stats
```

* get the counts of data loaded
```bash
python scripts/fhir-util.py count-resources 
```

* query resource counts:

```bash
python scripts/fhir-util.py count-resources
```

* ask the server to reindex the data (takes a while)

```bash
curl -X POST $AUTH $FHIR_BASE'/$reindex'
# monitor HAPI logs for progress
# when complete ask server for aggregated counts
python fhir-util.py get-resource-counts 

```

