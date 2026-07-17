FROM alpine/curl:8.19.0

WORKDIR /app

COPY connectors/ ./connectors/
COPY setup-connectors.sh .
RUN apk add --no-cache bash jq
# RUN echo "--- Verifying files inside /app ---" && ls -la
RUN chmod +x setup-connectors.sh

ENTRYPOINT ["/bin/bash", "./setup-connectors.sh"]
