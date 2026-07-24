# Domain Rules: Docker & Container Builds

Whenever working on a Dockerfile or container build within this repository, you must adhere to the following absolute constraints:

## 1. Multi-Stage Builds

- Separate the build stage (compilers, dev dependencies, build tools) from the runtime stage; the final image must not contain build-only artifacts.
- Copy only the compiled output/artifacts from the build stage into the runtime stage with `COPY --from=<build-stage>`.

## 2. Base Image Selection

- Use `slim`, `alpine`, or distroless base images for the runtime stage; only use full base images (e.g. `ubuntu`, `debian`) in the build stage if a compiler toolchain requires it.
- Always pin an exact tag (e.g. `node:20.11.1-slim`, not `node:latest` or `node:20`); floating tags break reproducibility and silently change behavior on rebuild.

## 3. Layer Caching Order

- Copy dependency manifests (`package.json`/`package-lock.json`, `go.mod`/`go.sum`, `requirements.txt`, `Cargo.toml`/`Cargo.lock`) and install dependencies before copying the rest of the source tree.
- Order `COPY`/`RUN` instructions from least-frequently-changed to most-frequently-changed so Docker's layer cache is invalidated only for what actually changed.

## 4. Non-Root User

- The final runtime stage must run as a non-root user; create a dedicated user/group (`RUN useradd -r -u 1001 appuser`) and set `USER appuser` before `CMD`/`ENTRYPOINT`.
- Never leave the default `root` user in a production image, and never rely on `--user` at `docker run` time as the only safeguard.

## 5. .dockerignore Discipline

- Every Dockerfile must be paired with a `.dockerignore` that excludes `.git`, local dependency directories (`node_modules/`, `target/`, `vendor/`), build output, `.env` files, and secrets.
- Never let secrets, credentials, or `.env` files reach the build context; if a secret is needed at build time, use Docker BuildKit secrets (`--mount=type=secret`), not `ARG`/`ENV` with the literal value.
