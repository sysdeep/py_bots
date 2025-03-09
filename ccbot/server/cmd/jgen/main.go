/*
- https://github.com/dgrijalva/jwt-go/blob/master/http_example_test.go
- https://golang-jwt.github.io/jwt/usage/parse/
*/
package main

import (
	"fmt"
	"os"

	"github.com/golang-jwt/jwt/v5"
)

func main() {
	signBytes, err := os.ReadFile("../../../private.pem")
	check_err(err)

	signKey, err := jwt.ParseRSAPrivateKeyFromPEM(signBytes)
	check_err(err)

	verifyBytes, err := os.ReadFile("../../../public.pem")
	check_err(err)

	// TODO: тут какая то беда....
	verifyKey, err := jwt.ParseRSAPrivateKeyFromPEM(verifyBytes)
	check_err(err)
	fmt.Println(verifyKey)

	// create token
	t := jwt.New(jwt.SigningMethodRS256)
	token, err := t.SignedString(signKey)
	check_err(err)

	fmt.Println(token)

	// // check token
	// tt, err := jwt.ParseWithClaims(token, *&jwt.RegisteredClaims{}, func(t *jwt.Token) (interface{}, error) {
	// 	return verifyKey, nil
	// })
	// check_err(err)
	// fmt.Println(tt)

}

func check_err(e error) {
	if e != nil {
		panic(e)
	}
}
