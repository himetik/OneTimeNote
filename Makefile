dev-start:
		@sudo docker-compose build && sudo docker-compose up
start:
		@sudo docker-compose build && sudo docker-compose up -d
stop:
		@sudo docker-compose down
clean:
		@find . -type f -name "*.pyc" -delete
		@find . -type f -name "*.log" -delete
		@sudo docker system prune -f
