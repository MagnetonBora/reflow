.PHONY: producer consumer kafka down

producer:
	python producer/producer.py

consumer:
	python consumer/consumer.py

kafka:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down
