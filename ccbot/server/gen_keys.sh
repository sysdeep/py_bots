#!/bin/bash

openssl genrsa -out id_rsa 4096
openssl rsa -in id_rsa -pubout -out id_rsa.pub
