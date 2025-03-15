package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

/*
данный вариант сработал
*/
func v2() {
	fmt.Println("\nV2\n")

	prvKey, err := os.ReadFile("../../../id_rsa")
	check_err(err)

	key, err := jwt.ParseRSAPrivateKeyFromPEM(prvKey)
	check_err(err)

	now := time.Now().UTC()
	ttl := time.Hour

	claims := make(jwt.MapClaims)
	claims["dat"] = "custom data"       // Our custom data.
	claims["exp"] = now.Add(ttl).Unix() // The expiration time after which the token must be disregarded.
	claims["iat"] = now.Unix()          // The time at which the token was issued.
	claims["nbf"] = now.Unix()          // The time before which the token must be disregarded.

	token, err := jwt.NewWithClaims(jwt.SigningMethodRS256, claims).SignedString(key)
	check_err(err)

	// // 1. Create a new JWT token.
	// tok, err := jwtToken.Create(time.Hour, "Can be anything")
	// if err != nil {
	// 	log.Fatalln(err)
	// }
	fmt.Println("TOKEN:", token)

	// validate ---------------------------------------------------------------
	pubKey, err := os.ReadFile("../../../id_rsa.pub")
	check_err(err)

	pub_key, err := jwt.ParseRSAPublicKeyFromPEM(pubKey)
	check_err(err)

	tok, err := jwt.Parse(token, func(jwtToken *jwt.Token) (interface{}, error) {
		if _, ok := jwtToken.Method.(*jwt.SigningMethodRSA); !ok {
			return nil, fmt.Errorf("unexpected method: %s", jwtToken.Header["alg"])
		}

		return pub_key, nil
	})
	check_err(err)

	claims, ok := tok.Claims.(jwt.MapClaims)
	if !ok || !tok.Valid {
		log.Fatal("validate: invalid")
	}

	fmt.Println(tok.Valid)
	fmt.Println(claims)

	// // 2. Validate an existing JWT token.
	// content, err := jwtToken.Validate(tok)
	// if err != nil {
	// 	log.Fatalln(err)
	// }
	// fmt.Println("CONTENT:", content)
}

func v1() {
	fmt.Println("\nV1\n")

	signBytes, err := os.ReadFile("../../../private.pem")
	check_err(err)

	signKey, err := jwt.ParseRSAPrivateKeyFromPEM(signBytes)
	check_err(err)

	// create token
	t := jwt.New(jwt.SigningMethodRS256)
	token, err := t.SignedString(signKey)
	check_err(err)

	fmt.Println("=============================")
	fmt.Println(token)
	fmt.Println("=============================")

	// check token

	verifyBytes, err := os.ReadFile("../../../public.pem")
	check_err(err)

	// TODO: тут какая то беда....
	// verifyKey, err := jwt.ParseRSAPrivateKeyFromPEM(verifyBytes)
	verifyKey, err := jwt.ParseRSAPublicKeyFromPEM(verifyBytes)
	check_err(err)
	// fmt.Println(verifyKey)

	// tt, err := jwt.ParseWithClaims(token, *&jwt.RegisteredClaims{}, func(t *jwt.Token) (interface{}, error) {
	tt, err := jwt.Parse(token, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodRSA); !ok {
			return nil, fmt.Errorf("unexpected method: %s", t.Header["alg"])
		}
		return verifyKey, nil
	})
	check_err(err)
	fmt.Println(tt.Valid)

}

/*
шифруем одним, расшифровываем другим - ожидается ошибка
*/
func v3_dif_keys() {
	fmt.Println("\nV3\n")

	signBytes, err := os.ReadFile("../../../private.pem")
	check_err(err)

	signKey, err := jwt.ParseRSAPrivateKeyFromPEM(signBytes)
	check_err(err)

	// create token
	t := jwt.New(jwt.SigningMethodRS256)
	token, err := t.SignedString(signKey)
	check_err(err)

	fmt.Println("=============================")
	fmt.Println(token)
	fmt.Println("=============================")

	// check token

	verifyBytes, err := os.ReadFile("../../../id_rsa.pub")
	check_err(err)

	// TODO: тут какая то беда....
	// verifyKey, err := jwt.ParseRSAPrivateKeyFromPEM(verifyBytes)
	verifyKey, err := jwt.ParseRSAPublicKeyFromPEM(verifyBytes)
	check_err(err)
	// fmt.Println(verifyKey)

	// tt, err := jwt.ParseWithClaims(token, *&jwt.RegisteredClaims{}, func(t *jwt.Token) (interface{}, error) {
	tt, err := jwt.Parse(token, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodRSA); !ok {
			return nil, fmt.Errorf("unexpected method: %s", t.Header["alg"])
		}
		return verifyKey, nil
	})
	check_err(err)
	fmt.Println(tt.Valid)

}
