files := main.c
out := usbdrv

run: $(out)
	./$(out)

clean: $(out)
	rm $(out)

$(out): $(files)
	gcc -o$(out) $(files)
