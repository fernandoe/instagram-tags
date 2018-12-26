TRAVIS_REPO_SLUG ?= fernandoe/fe-instagram-api
TAG ?= local

build:
	docker build -t '${TRAVIS_REPO_SLUG}:${TAG}' .

ci.test:
	true
#	docker run --rm -it '${TRAVIS_REPO_SLUG}:${TAG}' pytest -s

compose-build:
	docker-compose build api-instagram

compose-up:
	docker-compose up

compose-migrate:
	docker-compose run --rm hashtags python manage.py migrate

compose-makemigrations:
	docker-compose run --rm hashtags python manage.py makemigrations

compose-createsuperuser:
	docker-compose run --rm hashtags python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@example.com', 'password')"

compose-extract_tags:
	docker-compose run --rm hashtags python manage.py extract_tags

compose-delete_invalid_tags:
	docker-compose run --rm hashtags python manage.py delete_invalid_tags

compose-shell:
	docker-compose run --rm hashtags sh
