package system

import (
	"log/slog"
	"net/http"

	"github.com/labstack/echo/v4"
)

type api struct {
	s *service
}

func newApi(e *echo.Group, s *service) *api {

	a := &api{s}

	e.GET("/service/:code/:action", a.Service)
	// e.GET("/stop", a.Stop)
	// e.GET("/start", a.Start)
	// e.GET("/restart", a.Restart)

	return a
}

func (a *api) Service(c echo.Context) error {
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
