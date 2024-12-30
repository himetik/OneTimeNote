dev-start:
		@sudo docker-compose build && sudo docker-compose up
up:
		@sudo docker-compose build && sudo docker-compose up -d
down:
		@sudo docker-compose down
clean:
		@find . -type f -name "*.pyc" -delete
		@find . -type f -name "*.log" -delete
		@sudo docker system prune -f
