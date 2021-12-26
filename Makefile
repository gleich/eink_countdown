build:
	GOOS=linux GOARCH=arm go build -v -o ./bin/oled_countdown .

deploy: build
	scp ./bin/oled_countdown pi@mg03.local:/home/pi/oled_countdown