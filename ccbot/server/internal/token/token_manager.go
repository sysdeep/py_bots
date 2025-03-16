/*
- https://www.inanzzz.com/index.php/post/kdl9/creating-and-validating-a-jwt-rsa-token-in-golang
*/
package token

import (
	"crypto/rsa"
	"fmt"

	"github.com/golang-jwt/jwt/v5"
)

type TokenManager struct {
	privateKey *rsa.PrivateKey
	publicKey  *rsa.PublicKey
}

func New(privateKey, publicKey []byte) (*TokenManager, error) {

	priKey, err := jwt.ParseRSAPrivateKeyFromPEM(privateKey)
	if err != nil {
		return nil, err
	}

	pubKey, err := jwt.ParseRSAPublicKeyFromPEM(publicKey)
	if err != nil {
		return nil, err
	}

	return &TokenManager{
		privateKey: priKey,
		publicKey:  pubKey,
	}, nil
}

func (m *TokenManager) GetKey(token *jwt.Token) (interface{}, error) {
	if _, ok := token.Method.(*jwt.SigningMethodRSA); !ok {
		return nil, fmt.Errorf("unexpected method: %s", token.Header["alg"])
	}

	return m.publicKey, nil
}

func (m *TokenManager) ReadClaims(token *jwt.Token) (Payload, error) {

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok || !token.Valid {
		return Payload{}, fmt.Errorf("validate: invalid")
	}

	// fmt.Println(tok.Valid)
	// fmt.Println(claims)
	ttype, ok := claims["type"]
	if !ok {
		return Payload{}, fmt.Errorf("token type not found")
	}

	return Payload{
		TType: int(ttype.(float64)),
	}, nil
}

// func (m *TokenManager) Read(token string) (Payload, error) {
// 	tok, err := jwt.Parse(token, func(jwtToken *jwt.Token) (interface{}, error) {
// 		if _, ok := jwtToken.Method.(*jwt.SigningMethodRSA); !ok {
// 			return nil, fmt.Errorf("unexpected method: %s", jwtToken.Header["alg"])
// 		}

// 		return m.publicKey, nil
// 	})

// 	if err != nil {
// 		return Payload{}, err
// 	}

// 	claims, ok := tok.Claims.(jwt.MapClaims)
// 	if !ok || !tok.Valid {
// 		return Payload{}, fmt.Errorf("validate: invalid")
// 	}

// 	// fmt.Println(tok.Valid)
// 	// fmt.Println(claims)
// 	ttype, ok := claims["type"].(int)
// 	if !ok {
// 		return Payload{}, fmt.Errorf("token type not found")
// 	}

// 	return Payload{
// 		TType: ttype,
// 	}, nil
// }
