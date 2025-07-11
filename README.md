# 🚀 Hello ArgoCD: GitOps Deployment on Local Kubernetes

This project demonstrates how to build a simple Python web app, containerize it, push the Docker image to a registry, and deploy it on a local Kubernetes cluster using **Argo CD** and **GitOps** principles.

---

## 📦 Stack

* Python 3
* Docker + Docker Hub
* Kubernetes (via Docker Desktop on macOS)
* Argo CD
* Git (GitHub, GitLab, etc.)

---

## 🧰 Prerequisites

Ensure the following are installed:

* [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)

  * Enable Kubernetes in Docker Desktop → Settings → Kubernetes
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

  ```bash
  brew install kubectl
  ```
* [Argo CD CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/)

  ```bash
  brew install argocd
  ```
* [Git](https://git-scm.com/)

---

## 🧱 Step 1: Create and Test the Hello World App

### 1. Create project folder

```bash
mkdir hello-argo && cd hello-argo
```

### 2. Create `app.py`

```python
# app.py
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from ArgoCD!")

server = HTTPServer(('0.0.0.0', 8080), Handler)
print("Listening on 8080")
server.serve_forever()
```

### 3. Create `Dockerfile`

```Dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

### 4. Build and test locally

```bash
docker build -t hello-argo:local .
docker run -p 8080:8080 hello-argo:local
```

Visit [http://localhost:8080](http://localhost:8080) — you should see:

```
Hello from ArgoCD!
```

---

## 🐳 Step 2: Push Docker Image to Docker Hub

### 1. Login to Docker Hub

```bash
docker login
```

### 2. Tag your image

```bash
docker tag hello-argo:local yourusername/hello-argo:latest
```

### 3. Push the image

```bash
docker push yourusername/hello-argo:latest
```

---

## 📁 Step 3: Prepare Kubernetes Manifests

### Create `k8s/` folder with:

#### `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-argo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-argo
  template:
    metadata:
      labels:
        app: hello-argo
    spec:
      containers:
        - name: web
          image: yourusername/hello-argo:latest
          ports:
            - containerPort: 8080
```

#### `k8s/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-argo
spec:
  selector:
    app: hello-argo
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: NodePort
```

---

## 📂 Step 4: Initialize and Push Git Repository

```bash
git init
git add .
git commit -m "Initial commit with app, Dockerfile, and Kubernetes manifests"
git remote add origin https://github.com/YOUR_USERNAME/hello-argo.git
git push -u origin main
```

---

## 🚀 Step 5: Install Argo CD on Local Kubernetes

### 1. Apply Argo CD installation manifest

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Port-forward Argo CD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Access [https://localhost:8080](https://localhost:8080)

### 3. Get the initial admin password

```bash
kubectl get secret argocd-initial-admin-secret -n argocd \
  -o jsonpath="{.data.password}" | base64 -d
```

Login via Argo CD CLI:

```bash
argocd login localhost:8080
argocd account update-password
```

---

## 📱 Step 6: Deploy App with Argo CD

### 1. Create Argo CD Application

```bash
argocd app create hello-argo \
  --repo https://github.com/YOUR_USERNAME/hello-argo.git \
  --path k8s \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default
```

### 2. Sync the app

```bash
argocd app sync hello-argo
```

### 3. Check the app status

```bash
argocd app get hello-argo
```

---

## ✅ Access the App

```bash
kubectl get svc
```

Find the `NodePort` assigned to `hello-argo`, then visit:

```
http://localhost:<nodePort>
```

You should see: `Hello from ArgoCD!`

---

## 🔄 Optional: Enable Auto-Sync

```bash
argocd app set hello-argo --sync-policy automated
```

---

## 🧪 Bonus: Clean Up

```bash
argocd app delete hello-argo
kubectl delete namespace argocd
```

---

## 📘 References

* [Argo CD Docs](https://argo-cd.readthedocs.io/)
* [Kubernetes Docs](https://kubernetes.io/docs/)
* [Docker Docs](https://docs.docker.com/)

