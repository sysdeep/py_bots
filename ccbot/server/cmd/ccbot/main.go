package main

import (
	"context"
	"flag"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"nia.pro/ccbot_server/internal/token"
	"nia.pro/ccbot_server/internal/webserver"
)

const (
	SHUTDOWN_TIMEOUT int = 5
)

func main() {
	slog.Info("start app")

	privateKeyPtr := flag.String("private-key", "", "path to private key")
	publicKeyPtr := flag.String("public-key", "", "path to public key")

	flag.Parse()

	if len(*privateKeyPtr) == 0 {
		slog.Error("no private key specifed")
		os.Exit(1)
	}

	if len(*publicKeyPtr) == 0 {
		slog.Error("no public key specifed")
		os.Exit(1)
	}

	// token manager ----------------------------------------------------------
	privateKeyBytes, err := os.ReadFile(*privateKeyPtr)
	check_err(err)

	publicKeyBytes, err := os.ReadFile(*publicKeyPtr)
	check_err(err)

	token_manager, err := token.New(privateKeyBytes, publicKeyBytes)
	check_err(err)

	// webserver --------------------------------------------------------------
	ws_config := webserver.WebserverConfig{Host: "0.0.0.0", Port: 7788}
	ws := webserver.New(ws_config, token_manager)

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

func check_err(err error) {
	if err != nil {
		slog.Error(err.Error())
		os.Exit(1)
	}
}
