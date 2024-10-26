FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY app.py .
COPY .python-version .
COPY pyproject.toml .

RUN uv sync -v

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["uv", "run", "app.py"]

# docker build -t andersonlkarl/fractal-uv-python:1.0 .
# docker run -p 7860:7860 andersonlkarl/fractal-uv-python:1.0