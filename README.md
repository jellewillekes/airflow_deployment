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
│   └── hello_world_minio.py    # Simple example Airflow DAG
├── k8s-manifests/
│   ├── airflow-scheduler.yaml
│   ├── airflow-webserver.yaml
│   ├── minio.yaml
│   └── minio-dag-sync.yaml
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

### 1. Create the Kubernetes cluster

```bash
kind create cluster --name kind-airflow-cluster
```

### 2. Create namespaces

```bash
kubectl create namespace airflow
kubectl create namespace minio-dev
```

### 3. Deploy MinIO, Airflow and the DAG sync

```bash
kubectl apply -f k8s-manifests/minio.yaml
kubectl apply -f k8s-manifests/minio-dag-sync.yaml
kubectl apply -f k8s-manifests/airflow-scheduler.yaml
kubectl apply -f k8s-manifests/airflow-webserver.yaml
```

---

## Uploading your DAGs

> Upload DAG file **manually using the MinIO console**.

1. Open the MinIO Console:
    ```bash
    kubectl port-forward svc/minio -n minio-dev 9000:9000 9001:9001
    ```
    Visit: http://localhost:9001  
    Login: `minioadmin` / `minioadmin`

2. Upload your DAG file (e.g. `hello_world_minio.py`) into the `airflow-dags` bucket.

3. The DAG sync daemon will automatically copy it to `/mnt/airflow-dags` on your nodes.

---

## Accessing Airflow

```bash
kubectl port-forward svc/airflow-service -n airflow 8080:8080
```

Visit: http://localhost:8080  
Login: `admin` / `admin`

---

## Checking logs and errors

### View the Airflow scheduler logs

```bash
kubectl logs -n airflow -f $(kubectl get pods -n airflow -l app=airflow-scheduler -o jsonpath='{.items[0].metadata.name}')
```

### Check import errors

```bash
kubectl exec -it -n airflow $(kubectl get pods -n airflow -l app=airflow-scheduler -o jsonpath='{.items[0].metadata.name}') -- airflow dags list-import-errors
```

### List your DAGs

```bash
kubectl exec -it -n airflow $(kubectl get pods -n airflow -l app=airflow-scheduler -o jsonpath='{.items[0].metadata.name}') -- airflow dags list
```

---

## Clean up

```bash
kind delete cluster --name kind-airflow-cluster
```

---

## Notes

- This is a local dev setup using `hostPath` and `SequentialExecutor`.  
- For production use PVCs and CeleryExecutor / KubernetesExecutor.
