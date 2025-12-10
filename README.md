# Speech language identification API service
This project hosts and serves the best-performing car price prediction model from the [training project](https://github.com/1roma1/speech-language-identification).

## Getting Started
Follow these steps to set up the project and run the pipelines.

### Prerequisites
You need Python 3.13 and uv packet manager installed.

### Installation
1. Clone the repository
```
git clone https://github.com/1roma1/speech-language-identification-api
```
2. Create a virtual environment and install dependencies
```
uv sync
```
3. Set up enviromental variables:
- `MLFLOW_TRACKING_URI`
- `MLFLOW_TRACKING_USERNAME` 
- `MLFLOW_TRACKING_PASSWORD`

### Run the service locally
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The API service will be accessible at `http://127.0.0.1:8000`

## API Endpoints

### 1. Health Check
| Endpoint | Method | Description |
| --- | --- | --- |
| `/health `| `GET` |  Return a simple status `{"status": "ok"}` to confirm the srvice is running.

### 2. Prediction Endpoint
| Endpoint | Method | Description |
| --- | --- | --- |
| `/predict `| `POST` |  Accepts a wav file and returns the predicted language.


**Example Response (JSON)**
```
{
  "language": "English"
}
```
## Deploy
1. Build Docker container
```
docker build -t romansaiko/romansaiko/speech-lang-id-api .
```
2. Push the container to DockerHub
```
docker push romansaiko/romansaiko/speech-lang-id-api
```
3. Connect to remote VPS server
```
ssh username@ipaddress
```
4. Stop running docker container and remove image
```
docker kill containerid
docker rmi romansaiko/romansaiko/speech-lang-id-api
```
5. Pull new container and run it
```
docker pull romansaiko/romansaiko/speech-lang-id-api
docker run -d -p 127.0.0.1:8080:8080 --env-file .env romansaiko/romansaiko/speech-lang-id-api
```