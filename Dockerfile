FROM python:alpine AS builder

WORKDIR /src

# Copy only the files needed for pip install
COPY setup.py pyproject.toml MANIFEST.in ./
COPY inforsuitelb_sec/ ./inforsuitelb_sec/

RUN python -m pip install --only-binary=:all: build==1.2.2.post1 setuptools==75.8.0 wheel==0.45.1 \
    && python -m build --wheel --no-isolation

FROM python:alpine

WORKDIR /src

COPY --from=builder /src/dist/*.whl /tmp/

RUN python -m pip install --only-binary=:all: \
        Jinja2==3.1.6 ConfigArgParse==1.7.5 redoctor==0.1.5 \
    && python -m pip install --only-binary=:all: --no-deps /tmp/*.whl \
    && rm /tmp/*.whl

USER nobody

ENTRYPOINT ["inforsuitelb_sec"]
