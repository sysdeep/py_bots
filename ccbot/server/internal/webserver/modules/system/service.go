package system

import (
	"errors"
	"log/slog"
	"os/exec"
)

// enums
const (
	CODE_WIREGUARD string = "eev3gu7A"
	CODE_NGINX     string = "usahgaL0"
)

const (
	ACTION_START   string = "xaequ9Ai"
	ACTION_STOP    string = "ahtaet1X"
	ACTION_STATUS  string = "shiKaip2"
	ACTION_RESTART string = "ooZ1aega"
)

// service
type service struct {
	services_map map[string]string
}

func newService() *service {

	var services_map map[string]string = map[string]string{}
	services_map[CODE_WIREGUARD] = "wg-quick@wg0.service"
	services_map[CODE_NGINX] = "nginx"

	return &service{services_map: services_map}
}

func (s *service) serviceAction(code string, action string) (string, error) {

	service_name, ok := s.services_map[code]
	if !ok {
		return "", errors.New("no code registered")
	}

	switch action {
	case ACTION_START:
		return s.doStart(service_name)

	case ACTION_STOP:
		return s.doStop(service_name)

	case ACTION_STATUS:
		return s.doStatus(service_name)

	case ACTION_RESTART:
		return s.doRestart(service_name)

	default:
		return "", errors.New("no action registered")
	}

}

// TODO: при запросе статуса сервиса который остановлен возвращается - exit status 3 без самимх данных, 3 - это код возврата операции
func (s *service) doStatus(service_name string) (string, error) {
	slog.Info("Status for " + service_name)
	cmd := exec.Command("systemctl", "status", service_name, "--plain", "--no-pager")
	out, err := cmd.CombinedOutput()

	return string(out), err
}

func (s *service) doStart(service_name string) (string, error) {
	slog.Info("Start for " + service_name)
	cmd := exec.Command("systemctl", "start", service_name, "--plain", "--no-pager")
	out, err := cmd.CombinedOutput()

	return string(out), err
}

func (s *service) doStop(service_name string) (string, error) {
	slog.Info("Stop for " + service_name)
	cmd := exec.Command("systemctl", "stop", service_name, "--plain", "--no-pager")
	out, err := cmd.CombinedOutput()

	return string(out), err
}

func (s *service) doRestart(service_name string) (string, error) {
	slog.Info("Restart for " + service_name)
	cmd := exec.Command("systemctl", "restart", service_name, "--plain", "--no-pager")
	out, err := cmd.CombinedOutput()

	return string(out), err
}
