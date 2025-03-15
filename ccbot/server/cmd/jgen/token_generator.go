package main

import (
	"github.com/golang-jwt/jwt/v5"
)

func createToken(keyBytes []byte) (string, error) {

	key, err := jwt.ParseRSAPrivateKeyFromPEM(keyBytes)
	check_err(err)

	// now := time.Now().UTC()
	// ttl := time.Hour

	claims := make(jwt.MapClaims)
	claims["type"] = TOKEN_TYPE_FIRST // token type

	// claims["exp"] = now.Add(ttl).Unix() // The expiration time after which the token must be disregarded.
	// claims["iat"] = now.Unix()          // The time at which the token was issued.
	// claims["nbf"] = now.Unix()          // The time before which the token must be disregarded.

	return jwt.NewWithClaims(jwt.SigningMethodRS256, claims).SignedString(key)
}
