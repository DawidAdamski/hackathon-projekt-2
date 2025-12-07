SHELL := /bin/bash

DC := docker compose

.PHONY: up down  build

build:
	$(DC) up -d --build

up:
	$(DC) up -d

down:
	$(DC) down

