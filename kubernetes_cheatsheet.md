# ☸️ Kubernetes (kubectl) Cheat Sheet

A concise guide for managing clusters, pods, services, and deployments with `kubectl`.

---

## ⚙️ SETUP & CONTEXT

```bash
kubectl version --client
kubectl config view
kubectl config get-contexts
kubectl config use-context my-cluster
kubectl cluster-info
kubectl get nodes
```

---

## 🧱 PODS

```bash
kubectl get pods
kubectl get pods -o wide
kubectl describe pod mypod
kubectl logs mypod
kubectl exec -it mypod -- /bin/bash
kubectl delete pod mypod
kubectl run nginx --image=nginx --port=80
```

### **Debug Pod**
```bash
kubectl run -it debug --image=alpine -- sh
```

---

## 🚀 DEPLOYMENTS

```bash
kubectl create deployment web --image=nginx
kubectl get deployments
kubectl describe deployment web
kubectl scale deployment web --replicas=3
kubectl rollout status deployment/web
kubectl rollout undo deployment/web
kubectl delete deployment web
```

---

## 🧩 SERVICES

```bash
kubectl expose deployment web --type=LoadBalancer --port=80 --target-port=8080
kubectl get services
kubectl describe service web
kubectl delete service web
```

### **Port Forwarding**
```bash
kubectl port-forward deployment/web 8080:80
```

---

## 📦 CONFIGMAPS & SECRETS

### **ConfigMap**
```bash
kubectl create configmap app-config --from-literal=MODE=production
kubectl get configmaps
kubectl describe configmap app-config
```

### **Secret**
```bash
kubectl create secret generic db-secret --from-literal=DB_PASS=StrongPassword123
kubectl get secrets
kubectl describe secret db-secret
kubectl get secret db-secret -o jsonpath="{.data.DB_PASS}" | base64 --decode
```

---

## 🧮 NAMESPACES

```bash
kubectl get namespaces
kubectl create namespace dev
kubectl delete namespace dev
kubectl get all -n dev
```

---

## 🌐 INGRESS & NETWORKING

```bash
kubectl get ingress
kubectl apply -f ingress.yaml
kubectl describe ingress my-ingress
kubectl delete ingress my-ingress
```

Example **ingress.yaml**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port:
                  number: 80
```

---

## 🧾 YAML EXAMPLES

### **Pod Definition**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx
      image: nginx:latest
      ports:
        - containerPort: 80
```

### **Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:latest
          ports:
            - containerPort: 80
```

---

## 🧰 VOLUMES & PERSISTENCE

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

Apply and use:
```bash
kubectl apply -f pvc.yaml
kubectl get pvc
```

---

## 🔍 MONITORING & DEBUGGING

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl top pods
kubectl describe node mynode
kubectl get all --all-namespaces
kubectl logs -f deployment/web
```

---

## 🪄 QUICK REFERENCE SUMMARY

| Task | Command |
|------|----------|
| List pods | `kubectl get pods` |
| Deploy app | `kubectl create deployment web --image=nginx` |
| Expose service | `kubectl expose deployment web --port=80 --type=LoadBalancer` |
| Scale deployment | `kubectl scale deployment web --replicas=3` |
| View logs | `kubectl logs -f podname` |
| Port forward | `kubectl port-forward deployment/web 8080:80` |
| Get all resources | `kubectl get all` |

---

## 💡 TIPS

- Use `-o yaml` to view resource definitions.
- Apply changes with `kubectl apply -f file.yaml`.
- Use `kubectl delete -f file.yaml` to clean up.
- Combine with Terraform for IaC pipelines.
- Use namespaces to isolate environments.
- Add `--context` flag to work across clusters.

---

**Created for:** Kubernetes cluster and container orchestration management  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #kubernetes #kubectl #containers #devops #cloud #automation
