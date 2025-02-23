package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"nia.pro/ccbot_server/internal/webserver"
)

const (
	SHUTDOWN_TIMEOUT int = 5
)

func main() {
	slog.Info("start app")

	// webserver --------------------------------------------------------------
	ws_config := webserver.WebserverConfig{Host: "0.0.0.0", Port: 7788}
	ws := webserver.New(ws_config)

	go func() {
		err := ws.Start()

		if err != nil && err != http.ErrServerClosed {
			slog.Error(err.Error())
			os.Exit(1)
		}
	}()

	// gracefull shutdown -----------------------------------------------------
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	slog.Info("waiting for stop signal...")

	<-ctx.Done()
	_, cancel := context.WithTimeout(context.Background(), time.Duration(SHUTDOWN_TIMEOUT)*time.Second)
	defer cancel()

	slog.Info("got stop signal")

	// stop webserver
	if err := ws.Shutdown(ctx); err != nil {
		slog.Error(err.Error())
		os.Exit(1)
	}

	slog.Info("finished")
	os.Exit(0)
}
