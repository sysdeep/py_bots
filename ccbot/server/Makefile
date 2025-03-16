run:
	go run ./cmd/ccbot --private-key ../../../secrets/id_rsa --public-key ../../../secrets/id_rsa.pub

build_with_cgo:
	go build --tags prod -o ccserver ./cmd/ccbot

build:
	CGO_ENABLED=0 go build --tags prod -o ccserver ./cmd/ccbot