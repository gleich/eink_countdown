package display

import (
	"github.com/gleich/lumber/v2"
	"periph.io/x/conn/v3/i2c/i2creg"
	"periph.io/x/devices/v3/ssd1306"
	"periph.io/x/host/v3"
)

func Setup(log lumber.Logger) (*ssd1306.Dev, error) {
	log.Info("Setting up display")
	_, err := host.Init()
	if err != nil {
		return nil, err
	}

	bus, err := i2creg.Open("")
	if err != nil {
		return nil, err
	}

	dev, err := ssd1306.NewI2C(bus, &ssd1306.Opts{W: 128, H: 32})
	if err != nil {
		return nil, err
	}

	log.Success("Setup display")
	return dev, nil
}
