package main

import (
	"time"

	"github.com/fogleman/gg"
	"github.com/gleich/lumber/v2"
	"github.com/gleich/oled_countdown/pkg/display"
)

func main() {
	log := lumber.NewCustomLogger()
	log.Timezone = time.Local

	disp, err := display.Setup(log)
	if err != nil {
		log.Fatal(err, "Failed to setup display")
	}

	ctx := gg.NewContext(disp.Bounds().Dx(), disp.Bounds().Dy())
	err = display.Clear(disp, ctx)
	if err != nil {
		log.Fatal(err, "Failed to clear display")
	}

	time.Sleep(3 * time.Second)
	log.Info("Haulting display")
	err = disp.Halt()
	if err != nil {
		log.Fatal(err, "Failed to stop using display")
	}
}
