#!/bin/bash

# add connect to aws session

run-black-reformat:
	black backend/ frontend/

build-backend:
	docker build --file=docker/backend/Dockerfile  -t twitter-backend .

build-frontend:
	docker build --file=docker/frontend/Dockerfile  -t twitter-frontend .