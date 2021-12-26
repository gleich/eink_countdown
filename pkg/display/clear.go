package display

import (
	"image"

	"github.com/fogleman/gg"
	"periph.io/x/devices/v3/ssd1306"
)

func Clear(disp *ssd1306.Dev, ctx *gg.Context) error {
	ctx.Clear()
	return disp.Draw(disp.Bounds(), ctx.Image(), image.Point{})
}
