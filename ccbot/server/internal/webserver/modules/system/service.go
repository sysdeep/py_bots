package system

import (
	"errors"
	"fmt"
	"log/slog"
	"os/exec"
)

// enums
const (
	CODE_WIREGUARD string = "eev3gu7A"
)

const (
	ACTION_START   string = "xaequ9Ai"
	ACTION_STOP    string = "ahtaet1X"
	ACTION_STATUS  string = "shiKaip2"
	ACTION_RESTART string = "ooZ1aega"
)

// service
type service struct {
}

func newService() *service {
	return &service{}
}

func (s *service) serviceAction(code string, action string) error {

	// var service_name string
	// var action string

	switch code {
	case CODE_WIREGUARD:
		fmt.Println("wireguard")
	default:
		return errors.New("no code registered")
	}

	switch action {
	case ACTION_START:
		fmt.Println("start")

	case ACTION_STOP:
		fmt.Println("stop")

	case ACTION_STATUS:
		fmt.Println("sttus")

	case ACTION_RESTART:
		fmt.Println("restart")

	default:
		return errors.New("no action registered")
	}

	// TODO: call action
	cmd := exec.Command("systemctl", "status", "syslog", "--output=json", "--plain", "--no-pager")
	out, err := cmd.CombinedOutput()
	if err != nil {
		slog.Error(err.Error())
	}
	fmt.Printf("%s\n", out)
	// TODO: get status

	return nil
}
