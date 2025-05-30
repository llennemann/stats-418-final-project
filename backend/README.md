Create a README.md file explaining what the project is and then additional directories (also with explanation READMEs) that contain your code, presentations, and any additional files of interest.

to push the docker image to dockerhub: 
- docker compose
docker buildx create --use
docker buildx build --platform linux/amd64 -t docker.io/llennema/418-final-project-traffic:latest . --push

dockerhub repo: llennema/418-final-project-traffic

