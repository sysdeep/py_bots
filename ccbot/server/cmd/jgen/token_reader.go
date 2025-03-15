package main

import (
	"fmt"

	"github.com/golang-jwt/jwt/v5"
)

func readToken(keyBytes []byte, token string) error {
	pub_key, err := jwt.ParseRSAPublicKeyFromPEM(keyBytes)
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
		return fmt.Errorf("validate: invalid")
	}

	fmt.Println(tok.Valid)
	fmt.Println(claims)
	return nil
}
