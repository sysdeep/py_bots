# CCBot server

Серверная часть управления

## Links

- https://dev.to/elioenaiferrari/asymmetric-cryptography-with-golang-2ffd
- https://pycryptodome.readthedocs.io/en/latest/src/examples.html#encrypt-data-with-rsa
- https://www.inanzzz.com/index.php/post/kdl9/creating-and-validating-a-jwt-rsa-token-in-golang

## Keygen

Сгенерировать пару ключей можно как go-утилитой keygen так и скриптом gen_keys.sh

```bash
go run ./cmd/jgen/ --generate --key ../../../private.pem > token_pem
go run ./cmd/jgen/ --verify --key ../../../public.pem --token ./token_pem
```
