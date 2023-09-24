# Macropad
CircuitPython for [Adafruit MacroPad RP2040](https://www.adafruit.com/product/5128)

## References
- https://learn.adafruit.com/macropad-hotkeys/custom-configurations
- https://learn.adafruit.com/adafruit-macropad-rp2040/macropad-keyboard-and-mouse
- https://docs.circuitpython.org/projects/macropad/en/latest/api.html
- https://docs.circuitpython.org/projects/hid/en/latest/
- https://docs.circuitpython.org/projects/hid/en/latest/examples.html#simple-gamepad

## To Do
- [x] get the screen rotated 90 degrees
- [x] add a way to include descriptions of key actions
- [ ] make a global value to track mouse movement
- [ ] key + rotary actions
    - [ ] undo/redo
    - [ ] cut/copy/paste/select-all
    - [ ] macro strings (lowercase them automatically?)
        - [ ] save: "CTRL + S"
        - [ ] command palette for VSCode: "CTRL + SHIFT + P"
    - [x] increase and decrease volume
    - [x] scroll through available layers
    - [ ] increase and decrease brightness
    - [ ] scrollwheel action
    - [ ] increase and decrease cursor speed
    - [ ] alias numbers, i.e.  1 or "1" to "one"
- [ ] layers
    - [ ] individual files for layer mappings
        - [ ] list parent layer
            - [ ] use this to sort layer list (children come after their parents)
        - [ ] define a color scheme and pattern for the layer
    - [ ] fallthrough to lower layers for key actions when those aren't assigned
    - [ ] lighting
        - [ ] custom lighting color and pattern for each layer
        - [ ] Layer Select layer shows those colors on the appropriate hotkeys
    - [ ] implement improved mousekeys as a layer
        - [ ] have a function that runs while it's being held?
            - [ ] hold functions increment a counter
- [x] rotary click input
    - [x] have default rotary mode per-layer
    - [x] default: click to enter Layer Select layer
    - [x] default: volume control on rotation
- [ ] keep breaking out different aspects of the code into different files
    - [x] file for layer mappings
    - [x] file for key actions
- [ ] see if the macropad can pretend to be more than one HID
- [ ] support for tap, two-tap, and hold actions
    - [ ] support for tap *and* hold layer switches
          ex. shift only for the next key or swap into shifted layer
          - [ ] flag for expected # of inputs
          - [ ] flag for elapsed time
          - [x] add a default time-until-rollback-to-sleep/default
          - [ ] roll back when either elapses
    - [ ] hold actions: use auto-layers to implement Leader keys
- [ ] work on incorporating a pomodoro timer using the time lib
    - [ ] show timer progress on the OLED
- [ ] count keypresses
- [ ] add key action for changing the audio in/out
    with the FxSound key combinations
- [ ] find the repo for the little ASCII python pet
    - [ ] see if we can render the cute faces to the OLED
- [ ] attach second OLED (can those be chained with other STEMMA QT boards?)
- [ ] split key functions and mapping from those to key names into a separate file
- [ ] support for a plover mode?