package webserver

import (
	"context"
	"fmt"
	"log/slog"
	"net/http"

	echojwt "github.com/labstack/echo-jwt/v4"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"nia.pro/ccbot_server/internal/token"
	"nia.pro/ccbot_server/internal/webserver/modules/system"
)

type Webserver struct {
	e      *echo.Echo
	config WebserverConfig
	tokenM *token.TokenManager
}

func New(config WebserverConfig, tokenM *token.TokenManager) *Webserver {

	e := echo.New()

	e.Use(middleware.LoggerWithConfig(middleware.LoggerConfig{
		Format: "method=${method}, uri=${uri}, status=${status}\n",
	}))

	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "hello")
	})

	// main api group
	api_route := e.Group("/api")
	jwt_config := echojwt.Config{
		KeyFunc: tokenM.GetKey,
	}
	api_route.Use(echojwt.WithConfig(jwt_config))

	// inti modules
	system.New(api_route.Group("/system"), tokenM)

	return &Webserver{
		e:      e,
		config: config,
		tokenM: tokenM,
	}
}

func (w *Webserver) Start() error {
	addr := fmt.Sprintf("%s:%d", w.config.Host, w.config.Port)
	slog.Info("запуск http сервера - " + addr)
	return w.e.Start(addr)
}

func (w *Webserver) Shutdown(ctx context.Context) error {
	slog.Info("webserver - shutdown")
	return w.e.Shutdown(ctx)
}
