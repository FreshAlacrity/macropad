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
- [ ] make a function that will ASCII up a cheat sheet for the layers?
- [x] add a way to include descriptions of key actions
- [x] make a global value to track mouse movement
    - [ ] add a specialized gaming-mouse layer where it accelerates over a bit of time and then decelerates over a bit of time for viewer comfort
        - [ ] add a per-layer mouse speed modifier
        - [ ] try damped harmonic oscillator mouse movement where it gently eases back a bit after the key is released
    - [ ] mouse_angular_move(theta) that calls mouse_move(cos(theta), sin(theta))
- [ ] key + rotary actions
    - [ ] open the CIRCUITPY drive
    - [ ] increase and decrease cursor speed
    - [ ] undo/redo
    - [ ] Discord hotkeys
    - [ ] cut/copy/paste/select-all
    - [ ] macro strings (lowercase them automatically?)
        - [ ] save: "CTRL + S"
        - [ ] command palette for VSCode: "CTRL + SHIFT + P"
    - [x] increase and decrease volume
    - [x] scroll through available layers
    - [ ] increase and decrease brightness
    - [ ] scrollwheel action
    - [ ] alias numbers, i.e.  1 or "1" to "one"
- [ ] layers
    - [x] fallthrough to parent layers for key actions when those aren't assigned
        - [ ] better parent layer function after individual file support
    - [ ] individual files for layer mappings
        - [x] list parent layer
            - [ ] use this to sort layer list (children come after their parents)
    - [x] lighting
        - [ ] custom lighting color per layer
        - [x] custom lighting pattern for each layer
        - [ ] Layer Select layer shows layer colors on the appropriate hotkeys
        - [ ] if no layer pattern is specified, light the keys that have layer-specific actions
    - [x] implement improved mousekeys as a layer
        - [x] have a function that runs while it's being held?
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
              - [ ] have the first keypress back from sleep do nothing
          - [ ] roll back to previous layer when either elapses
    - [ ] hold actions: use auto-layers to implement Leader keys

- [ ] count keypresses
- [ ] add key action for changing the audio in/out
    with the FxSound key combinations
- [ ] screen(s)
    - [ ] work on incorporating a pomodoro timer using the time lib
        - [ ] show timer progress on the OLED
    - [ ] figure out if there's a way to have a log in the serial pane/second OLED without printing to the main screen
    - [ ] find the repo for the little ASCII python pet
        - [ ] see if we can render the cute faces to the OLED
    - [ ] attach second OLED (can those be chained with other STEMMA QT boards?)
- [x] split key functions and mapping from those to key names into a separate file
- [ ] support for a plover mode?