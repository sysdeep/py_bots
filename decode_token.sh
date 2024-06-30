#!/bin/bash

NIKA_HELP_PHRASE=$1


openssl enc -k ${NIKA_HELP_PHRASE}  -aes256 -base64 -d -in token_debug.enc -out .token

