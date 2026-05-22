#!/bin/bash

CONNECT_URL="http://dapp-kafka-connect:8083"
CONNECTOR_DIR="./connectors"

CONNECTOR_FILES=(
  "stores-connector.json"
  "products-connector.json"
)

echo "Starting connector registration..."

for file in "${CONNECTOR_FILES[@]}"; do
  FULL_PATH="$CONNECTOR_DIR/$file"

  if [ ! -f "$FULL_PATH" ]; then
    echo "File not found: $FULL_PATH"
    continue
  fi

  # Extract connector name
  NAME=$(jq -r '.name' "$FULL_PATH")

  if [ -z "$NAME" ] || [ "$NAME" == "null" ]; then
    echo "Could not extract connector name from $file"
    continue
  fi

  # Extract config only (Kafka Connect PUT requires only .config)
  CONFIG=$(jq '.config' "$FULL_PATH")

  echo "Processing connector: $NAME"

  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    "$CONNECT_URL/connectors/$NAME")

  if [ "$STATUS" == "200" ]; then
    echo "Connector exists. Updating: $NAME"

    RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
      -H "Content-Type: application/json" \
      --data "$CONFIG" \
      "$CONNECT_URL/connectors/$NAME/config")

  else
    echo "Connector does not exist. Creating: $NAME"

    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
      -H "Content-Type: application/json" \
      --data @"$FULL_PATH" \
      "$CONNECT_URL/connectors")
  fi

  BODY=$(echo "$RESPONSE" | head -n 1)
  CODE=$(echo "$RESPONSE" | tail -n 1)

  if [[ "$CODE" == "200" || "$CODE" == "201" ]]; then
    echo "Success: $NAME"
  else
    echo "Failed: $NAME"
    echo "Response: $BODY"
  fi

  echo "-----------------------------------"
done

echo "Done."