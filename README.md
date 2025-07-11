
# Airflow + PostgreSQL + MinIO on Kubernetes (Kind)

[![Local Dev](https://img.shields.io/badge/env-local-blue)](https://kind.sigs.k8s.io/) 
[![Kubernetes](https://img.shields.io/badge/kubernetes-1.27+-blue?logo=kubernetes)](https://kubernetes.io/)
[![Airflow](https://img.shields.io/badge/apache%20airflow-2.8.2-blue?logo=apache-airflow)](https://airflow.apache.org/)
[![MinIO](https://img.shields.io/badge/minio-latest-orange?logo=minio)](https://min.io/)

---

## Project structure

```text
airflow_deployment/
├── dags/
│   └── hello_world.py      # Example Airflow DAG
├── deployment.yaml         # Deploys Airflow + PostgreSQL with DAGs mounted
├── minio_deployment.yaml   # Deploys MinIO (S3 compatible object store)
├── kind_config.yaml        # Kind cluster config (mounts local dags folder)
└── .gitignore
```

---

## Requirements

- Docker Desktop
- Kind (Kubernetes in Docker)
- kubectl
- Clone this repo:
  ```bash
  git clone https://github.com/jellewillekes/airflow_deployment.git
  cd airflow_deployment
  ```

---

## Running the deployment

### Create the Kubernetes cluster

```bash
kind create cluster --name kind-airflow-cluster --config kind_config.yaml
```

### Create namespaces

```bash
kubectl create namespace airflow
kubectl create namespace minio-dev
```

### Deploy Airflow + PostgreSQL

```bash
kubectl apply -f deployment.yaml
```

### Deploy MinIO

```bash
kubectl apply -f minio_deployment.yaml
```

### Access the UIs

#### Airflow UI

```bash
kubectl port-forward svc/airflow-service -n airflow 8080:8080
```
Visit: http://localhost:8080  
**Login:** `admin` / `admin`

#### MinIO Console

```bash
kubectl port-forward svc/minio -n minio-dev 9000:9000 9001:9001
```
Visit: http://localhost:9001  
**Login:** `minioadmin` / `minioadmin`

---

## Verifying the setup

- Your DAGs in `dags/` appear in Airflow.
- PostgreSQL backs the metadata DB.
- MinIO provides an S3-like store.

---

## Clean

```bash
kind delete cluster --name kind-airflow-cluster
```

---

## Notes

Not for production: uses `hostPath` and `SequentialExecutor`. For production use cloud PVCs and CeleryExecutor / KubernetesExecutor.

---
