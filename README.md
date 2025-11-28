# Reflow

**Reflow** is an educational Python application designed to stream the latest posts from Lemmy into Apache Kafka for learning and experimentation with data pipelines.

## Overview

This project demonstrates how to:  
- Fetch the latest posts from a specific Lemmy community using the [Lemmy API](https://join-lemmy.org/api/).  
- Stream community posts into an Apache Kafka topic.  
- Consume and display messages from Kafka, simulating a real-world data pipeline workflow.

**Note:** This application is strictly for educational purposes. It does not post content, comment, or interact with Lemmy users in any way. Only publicly available data is used.

## Message Format

Posts are published to Kafka in JSON format:  
```json
{
  "id": "post.id",
  "title": "post.title",
  "upvotes": "post.score"
}
````

Comments (sample/educational) are published in JSON format:

```json
{
  "id": "post.id",
  "comment": "post.comment"
}
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- A `.env` file with the following variables:
  ```
  COMMUNITY=<lemmy-community-name>
  KAFKA_BROKER=<kafka-broker-address>
  KAFKA_TOPIC=<kafka-topic-name>
  ```

### Quick Start with Makefile

The project includes a Makefile for convenient command execution:

```bash
# Start Kafka infrastructure
make kafka

# Run the producer (streams posts from Lemmy to Kafka)
make producer

# Run the consumer (reads messages from Kafka)
make consumer

# Stop all services
make down
```

### Docker Compose Network

The `docker-compose.yml` uses an external network `conduktor-net` for integration with other services. Make sure this network exists or create it:

```bash
docker network create conduktor-net
```

### Development Container

This project includes a devcontainer configuration for VS Code. To use it:

1. Install the "Dev Containers" extension in VS Code
2. Open the project in VS Code
3. Click "Reopen in Container" when prompted (or use Command Palette: "Dev Containers: Reopen in Container")

The devcontainer automatically connects to the `conduktor-net` network for seamless integration with local Kafka services.

## Project Structure

```
reflow/
├── producer/           # Lemmy to Kafka producer
│   ├── producer.py
│   ├── kafka_helpers.py
│   └── lemmy_helpers.py
├── consumer/           # Kafka consumer
│   └── consumer.py
├── .devcontainer/      # VS Code devcontainer config
│   ├── devcontainer.json
│   └── Dockerfile
├── docker-compose.yml  # Kafka infrastructure
├── Makefile           # Convenience commands
└── requirements.txt   # Python dependencies
```

## License

This project is for educational purposes only.
