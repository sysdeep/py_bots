package utils

import (
	"encoding/json"
	"fmt"
)

func PrintAsJson(data interface{}) {

	result, err := json.MarshalIndent(data, "", "    ")
	if err != nil {
		fmt.Println("ERROR: " + err.Error())
		return
	}

	fmt.Println(string(result))
}
