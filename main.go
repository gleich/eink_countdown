package main

import (
	"time"

	"github.com/gleich/lumber/v2"
	"github.com/gleich/oled_countdown/pkg/display"
)

func main() {
	log := lumber.NewCustomLogger()
	log.Timezone = time.Local

	connectedDisplay, err := display.Setup(log)
	if err != nil {
		log.Fatal(err, "Failed to setup display")
	}

	err = connectedDisplay.Halt()
	if err != nil {
		log.Fatal(err, "Failed to stop using display")
	}
}
