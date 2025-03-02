run:
	go run ./cmd/ccbot

build_with_cgo:
	go build --tags prod -o ccserver ./cmd/ccbot

build:
	CGO_ENABLED=0 go build --tags prod -o ccserver ./cmd/ccbot