PI_NAME="pi@mg02.local"

deploy:
	rsync -ravP --exclude='/.git' . $(PI_NAME):/home/pi/oled_countdown/