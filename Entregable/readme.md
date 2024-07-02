# Entregable Covid ETL

- Create of folders and download yml
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml'

mkdir -p ./{logs,dags,config,plugins,raw_data}

echo -e "AIRFLOW_UID=$(id -u)" >> ./.env


```

- Copy .env to dags folder
```bash
cp .env ./dags/
```


- Start project
```bash
docker compose up airflow-init
```
```bash
docker compose up
```
