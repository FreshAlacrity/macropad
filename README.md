# Macropad
CircuitPython for [Adafruit MacroPad RP2040](https://www.adafruit.com/product/5128)

## References
- https://learn.adafruit.com/macropad-hotkeys/custom-configurations
- https://learn.adafruit.com/adafruit-macropad-rp2040/macropad-keyboard-and-mouse
- https://docs.circuitpython.org/projects/macropad/en/latest/api.html
- https://docs.circuitpython.org/projects/hid/en/latest/

## To Do
- [x] get the screen rotated 90 degrees
- [ ] keep breaking out different aspects of the code into different files
    - [x] file for layer mappings
        - [ ] individual files for layer mappings
            - [ ] list parent layer
            - [ ] define a color scheme and pattern for the layer
    - [x] file for key actions
- [ ] see if the macropad can pretend to be more than one HID
- [ ] add a way to include descriptions of key actions
- [ ] support for tap, two-tap, and hold actions
    - [ ] support for tap and hold layer switches
          ex. shift only for the next key or swap into shifted layer
          flag for expected # of inputs or elapsed time, whichever is shorter
          add a default time-until-rollback-to-sleep/default
          def layer(inputs, time):
    - [ ] hold actions: support for 'listeners' for leader keys 
          without sending HID keycodes
- [ ] click rotary to change between rotary input modes
    - [ ] layer select mode
    - [ ] volume control mode
- [ ] implement improved mousekeys as a layer
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