#
# This is a project Makefile. It is assumed the directory this Makefile resides in is a
# project subdirectory.
#
.PHONY: ota

PROJECT_NAME := ledc_basic

include $(IDF_PATH)/make/project.mk

build:  main/main.c main/motor.c main/ota.c
	idf.py build

ota: build
	# TODO: ask cochecito API to perform OTA update
	openssl s_server -WWW -key ca_key.pem -cert ca_cert.pem -port 8070
