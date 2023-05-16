export DOCKER_BUILDKIT := "1"

run:
    uvicorn webhook:API \
        --host 0.0.0.0 \
        --port 10000 \
        --reload \
        --reload-dir ./webhook/


shell:
    python -i ./shell.py

tunnel:
    ngrok http 10000
