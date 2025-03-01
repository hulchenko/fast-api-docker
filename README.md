# AWS ECS deployment

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 851725465462.dkr.ecr.us-west-2.amazonaws.com

docker build -t fast-api-app .

docker tag fast-api-repo:latest 851725465462.dkr.ecr.us-west-2.amazonaws.com/fast-api-app:latest

docker push 851725465462.dkr.ecr.us-west-2.amazonaws.com/fast-api-repo:latest

# Kubernetes local deployment

minikube start

kubectl run fast-api-app --image=vadymhulchenko/vadym-test-repo:latest --port=8000

expose pod fast-api-app --name=fast-api-app-pod --port=8000

kubectl port-forward service/fast-api-app-pod 8000:8000
