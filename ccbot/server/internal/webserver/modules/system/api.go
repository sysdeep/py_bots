package system

import (
	"log/slog"
	"net/http"

	"github.com/labstack/echo/v4"
	"nia.pro/ccbot_server/internal/token"
)

type api struct {
	s      *service
	tokenM *token.TokenManager
}

func newApi(e *echo.Group, s *service, tokenM *token.TokenManager) *api {

	a := &api{
		s:      s,
		tokenM: tokenM,
	}

	e.GET("/service/:code/:action", a.Service)
	// e.GET("/stop", a.Stop)
	// e.GET("/start", a.Start)
	// e.GET("/restart", a.Restart)

	return a
}

func (a *api) Service(c echo.Context) error {

	// NOTE: see https://echo.labstack.com/docs/cookbook/jwt
	// token := c.Get("user").(*jwt.Token)
	// fmt.Println(a.tokenM.ReadClaims(token))

	code := c.Param("code")
	action := c.Param("action")

	result, err := a.s.serviceAction(code, action)
	if err != nil {
		slog.Error(err.Error())
		return c.String(http.StatusInternalServerError, err.Error())
	}

	return c.String(http.StatusOK, result)
}

// func (a *api) Stop(c echo.Context) error {
// 	return c.String(http.StatusOK, "service stop")
// }

// func (a *api) Start(c echo.Context) error {
// 	return c.String(http.StatusOK, "service start")
// }

// func (a *api) Restart(c echo.Context) error {
// 	return c.String(http.StatusOK, "service restart")
// }
