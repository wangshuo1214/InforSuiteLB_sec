FROM python:alpine

WORKDIR /app

# Copy source code and runtime dependencies
COPY requirements.txt ./
COPY inforsuitelb_sec/ ./inforsuitelb_sec/

# Install runtime dependencies directly (no wheel build step)
RUN python -m pip install --no-cache-dir --only-binary=:all: -r requirements.txt \
    && python -m pip install --no-cache-dir --only-binary=:all: redoctor==0.1.5

USER nobody

# Run directly via python -m (no pip-installed entry point)
ENTRYPOINT ["python", "-m", "inforsuitelb_sec.cli.main"]
