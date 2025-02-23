package core

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

type stdError struct {
	Error string `json:"error"`
}

func MakeStdError(c echo.Context, err error) error {
	return c.JSON(http.StatusInternalServerError, stdError{Error: err.Error()})
}
