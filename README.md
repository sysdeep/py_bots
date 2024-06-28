# py_bots

    pip install pytelegrambotapi

https://www.gitbook.com/book/groosha/telegram-bot-lessons/details

## Token encrypt

Токен хранится в зашифрованном виде в файле token.enc
Для использования его необходимо предварительно расшифровать командой `decode_token.sh PASSWORD`

Инструкции по шифрованию

```bash

# encrypt
openssl enc -k NIKA_HELP_PHRASE -aes256 -base64 -e -in .token -out token.enc

# decrypt
openssl enc -k NIKA_HELP_PHRASE  -aes256 -base64 -d -in token.enc -out .token

```
