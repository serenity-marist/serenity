
build:
	@docker build -t serenity-api .

app: build
	@docker run --rm --name api_dev -it -p8080:8080 serenity-api

publish-image: build
	@docker tag serenity-api ajavellana123/serenity-api:latest
	@docker push ajavellana123/serenity-api