# Macropad
CircuitPython for [Adafruit MacroPad RP2040](https://www.adafruit.com/product/5128)

## References
- https://learn.adafruit.com/macropad-hotkeys/custom-configurations
- https://learn.adafruit.com/adafruit-macropad-rp2040/macropad-keyboard-and-mouse

## To Do
- [x] get the screen rotated 90 degrees
- [ ] see if the macropad can pretend to be more than one HID
- [ ] click rotary to change between modes
    ex volume control and layer select
- [ ] add a layer system with layer select via rotary knob
    - [ ] implement improved mousekeys as a layer
- [ ] work on incorporating a pomodoro timer using the time lib
    - [ ] show timer progress on the OLED
- [ ] count keypresses
- [ ] add key action for changing the audio in/out
    with the FxSound key combinations
- [ ] use an array of keynames to map to key numbers
- [ ] find the repo for the little ASCII python pet
    - [ ] see if we can render the cute faces to the OLED
- [ ] attach second OLED (can those be chained with other STEMMA QT boards?)
- [ ] split key functions and mapping from those to key names into a separate file
