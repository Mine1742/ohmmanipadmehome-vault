# Kubernetes Overview & Beginner’s Guide

## 🌐 What is Kubernetes?  
Kubernetes (**K8s**) is an **open-source container orchestration platform** that helps you **deploy, manage, scale, and monitor** applications inside containers (e.g., Docker).  

It acts like an **operating system for your data center/cloud**, ensuring your apps run reliably, scale when needed, and recover automatically from failures.  

---

## 🔹 Key Concepts  

- **Cluster** – A group of machines (nodes).  
  - **Control Plane** (master): Manages the cluster.  
  - **Worker Nodes**: Run workloads.  

- **Pod** – Smallest deployable unit, runs one or more containers.  

- **Deployment** – Defines how Pods are created and managed (ensures desired state = actual state).  

- **Service** – Provides stable networking and load balancing for Pods.  

- **Namespace** – Logical separation of resources (projects, environments).  

- **ConfigMap & Secret** – Store configuration and sensitive data.  

---

## 🔹 Benefits of Kubernetes  

✅ **Scalability** – Auto-scaling up/down.  
✅ **Self-healing** – Restarts/reschedules failed Pods.  
✅ **Portability** – Runs across AWS, Azure, GCP, on-prem.  
✅ **Service Discovery & Load Balancing** – Stable networking.  
✅ **Declarative Configuration** – Desired state defined in YAML/JSON.  

---

## 🔹 Basic Workflow  

1. Write a **YAML manifest** describing your app (Pods, Deployments, Services).  
2. Deploy to cluster:  
   ```bash
   kubectl apply -f my-app.yaml
   ```  
3. Kubernetes schedules Pods across worker nodes.  
4. Access app via **Service** or **Ingress**.  

---

## 🔹 Example Deployment (YAML)  

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
```

Deploy and expose:  
```bash
kubectl apply -f nginx-deployment.yaml
kubectl get pods
kubectl expose deployment nginx-deployment --port=80 --type=NodePort
```

---

## 🔹 Common `kubectl` Commands  

```bash
# Cluster Info
kubectl cluster-info
kubectl get nodes

# Pods
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Deployments
kubectl get deployments
kubectl scale deployment nginx-deployment --replicas=5

# Services
kubectl get svc
```

---

## 🔹 Troubleshooting Guide

### ❌ Pod stuck in `CrashLoopBackOff`
- Run:  
  ```bash
  kubectl describe pod <pod-name>
  kubectl logs <pod-name>
  ```
- Common causes: bad image, missing env vars, app crash loop.  
- Fix: update Deployment YAML with correct image/config.

---

### ❌ Pod stuck in `Pending`
- Check if there are enough resources:  
  ```bash
  kubectl describe pod <pod-name>
  kubectl get nodes
  ```
- Often due to scheduling constraints (taints, affinity, resource limits).  

---

### ❌ Service not reachable
- Verify Service and Endpoints:  
  ```bash
  kubectl get svc
  kubectl describe svc <service-name>
  kubectl get endpoints <service-name>
  ```
- Check if Pods have correct labels to match the Service selector.  

---

### ❌ ImagePullBackOff
- Run:  
  ```bash
  kubectl describe pod <pod-name>
  ```
- Causes: wrong image name, missing registry secret, private repo.  
- Fix: correct image name or add secret with:  
  ```bash
  kubectl create secret docker-registry <name> --docker-username=... --docker-password=...
  ```

---

### ❌ DNS Resolution Issues
- Test DNS inside Pod:  
  ```bash
  kubectl exec -it <pod-name> -- nslookup kubernetes.default
  ```
- Ensure CoreDNS is running:  
  ```bash
  kubectl get pods -n kube-system -l k8s-app=kube-dns
  ```

---

## 🔹 When to Use Kubernetes  
- You manage **multiple microservices** that must scale independently.  
- You need **high availability & self-healing**.  
- You want **multi-cloud or hybrid deployments**.  

---

## 🔗 External Resources  
- [Kubernetes Official Docs](https://kubernetes.io/docs/)  
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)  
- [Play with Kubernetes (Free Lab)](https://labs.play-with-k8s.com/)  

---

## 🏷️ Tags  
#kubernetes #containers #cloud #devops #docker #orchestration #troubleshooting
