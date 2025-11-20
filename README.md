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

## Status

🚧 **Coming Soon**

The code and implementation will be available shortly. Stay tuned!

## License

This project is for educational purposes only.
