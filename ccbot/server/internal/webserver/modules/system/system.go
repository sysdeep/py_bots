package system

import "github.com/labstack/echo/v4"

type System struct {
	a *api
}

func New(e *echo.Group) *System {

	s := newService()

	return &System{
		a: newApi(e, s),
	}

}
