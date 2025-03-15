/*
jgen - генератор jwt токена

использование
jgen -generate --key ...
jgen -verify --key ... --token ...

go run ./cmd/jgen/ --generate --key ../../../private.pem > token_pem
go run ./cmd/jgen/ --verify --key ../../../public.pem --token ./token_pem

полезные ресурсы
- https://github.com/dgrijalva/jwt-go/blob/master/http_example_test.go
- https://golang-jwt.github.io/jwt/usage/parse/
*/
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

func main() {

	// parse flags
	actionGeneratePtr := flag.Bool("generate", false, "generate a new token")
	actionVerifyPtr := flag.Bool("verify", false, "verify a token")
	keyPtr := flag.String("key", "", "path to key")
	tokenPtr := flag.String("token", "", "path to token")

	flag.Parse()

	if *actionGeneratePtr {
		if len(*keyPtr) == 0 {
			log.Fatal("no key")
		}

		keyBytes, err := os.ReadFile(*keyPtr)
		check_err(err)

		token, err := createToken(keyBytes)
		check_err(err)
		fmt.Println(token)
		os.Exit(0)
	}

	if *actionVerifyPtr {
		if len(*keyPtr) == 0 {
			log.Fatal("no key")
		}

		if len(*tokenPtr) == 0 {
			log.Fatal("no token")
		}

		keyBytes, err := os.ReadFile(*keyPtr)
		check_err(err)

		tokenBytes, err := os.ReadFile(*tokenPtr)
		check_err(err)

		err = readToken(keyBytes, string(tokenBytes))
		check_err(err)
		// fmt.Println(token)
		os.Exit(0)

	}

	// run_tests()
}

func run_tests() {
	v1()
	v2()
	v3_dif_keys()
}

func check_err(e error) {
	if e != nil {
		panic(e)
	}
}
