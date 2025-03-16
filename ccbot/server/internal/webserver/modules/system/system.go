package system

import (
	"github.com/labstack/echo/v4"
	"nia.pro/ccbot_server/internal/token"
)

type System struct {
	a      *api
	tokenM *token.TokenManager
}

func New(e *echo.Group, tokenM *token.TokenManager) *System {

	s := newService()

	return &System{
		a:      newApi(e, s, tokenM),
		tokenM: tokenM,
	}

}
