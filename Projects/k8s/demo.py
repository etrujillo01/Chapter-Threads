# Arranca minikube o activa K8s en Docker Desktop
minikube start

# Ve a la carpeta k8s/
cd k8s

# Aplica todo (despliega en orden)
kubectl apply -f redis-deployment.yaml
kubectl apply -f api-deployment.yaml
kubectl apply -f worker-deployment.yaml

# Verifica que todo esté bien
kubectl get pods
kubectl get svc
kubectl get hpa

# Haz port-forward para probar API en localhost:8000
kubectl port-forward service/api-service 8000:8000

# Corre tu burst_stress.py para generar carga
python ../stress_testing_scripts/burst_stress.py 50

# Observa el auto-escalado en otra terminal
kubectl get hpa -w
kubectl get pods -w
