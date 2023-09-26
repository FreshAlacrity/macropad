# Macropad
CircuitPython for [Adafruit MacroPad RP2040](https://www.adafruit.com/product/5128)

## Design Concepts
tamtam in the keyboard is a pet we take care of when we take care of ourselves/a nudge to be more routine about self care, so it needs breaks from taking input and to be fed and watered and get enough sleep, and it'll cheerfully turn down the lights or refuse to take input if it needs a break
  - takes breaks only after sensible inputs (ESC, CTRL+S) when there's been ~25 minutes of activity recently
  - squeaks indignantly if you keep trying to use it during a break

## References
- https://learn.adafruit.com/circuitpython-display-support-using-displayio/sprite-sheet
- https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio
- https://learn.adafruit.com/macropad-hotkeys/custom-configurations
- https://learn.adafruit.com/adafruit-macropad-rp2040/macropad-keyboard-and-mouse
- https://docs.circuitpython.org/projects/macropad/en/latest/api.html
- https://docs.circuitpython.org/projects/hid/en/latest/
- https://docs.circuitpython.org/projects/hid/en/latest/examples.html#simple-gamepad
- [All supported keycodes](https://usb.org/sites/default/files/hut1_21_0.pdf#page=83)
  - note that keycodes are the names for key *positions* on a US keyboard

### Possible Fonts
- https://terminus-font.sourceforge.net/
- https://github.com/Tecate/bitmap-fonts
- https://github.com/benwr/glean
- https://github.com/cmvnd/fonts
- https://www.cl.cam.ac.uk/~mgk25/ucs-fonts.html
    - so far leads in support of most Unicode chars
- https://unifoundry.com/unifont/unifont-utilities.html

- Monospace
    - https://people.mpi-inf.mpg.de/~uwe/misc/uw-ttyp0/
        - nine sizes from 6x11 to 11x22 + bold versions; for some there is also a (somewhat experimental) italic
- see also https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display


### Useful Software
- https://github.com/rhinterndorfer/MousePointerReposition

### Misc
If pylance isn't recognizing imports from files, try Reload Window command

## To Do
- [ ] clean up multi-line comment examples
- [ ] have the backup and commit shortcut also close the explorer window
- [x] get the screen rotated 90 degrees
- [x] add a way to include descriptions of key actions
- [x] make a global value to track mouse movement
    - [ ] add a specialized gaming-mouse layer where it accelerates over a bit of time and then decelerates over a bit of time for viewer comfort
        - [ ] add a per-layer mouse speed modifier
        - [ ] try damped harmonic oscillator mouse movement where it gently eases back a bit after the key is released
    - [ ] mouse_angular_move(theta) that calls mouse_move(cos(theta), sin(theta))
- [ ] key + rotary actions
    - [ ] generic key-held actions (for arrow keys etc)
    - [x] open the CIRCUITPY drive
    - [ ] increase and decrease cursor speed
    - [ ] undo/redo
    - [ ] Discord hotkeys
    - [ ] cut/copy/paste/select-all
    - [x] macro strings
        - [ ] save: "CTRL + S"
        - [ ] command palette for VSCode: "CTRL + SHIFT + P"
    - [x] increase and decrease volume
    - [x] scroll through available layers
    - [ ] increase and decrease brightness
    - [ ] scrollwheel action
    - [ ] alias numbers, i.e.  1 or "1" to "one"
    - [ ] change audio in/out with FxSound key combinations
- [ ] layers
    - [x] fallthrough to parent layers for key actions when those aren't assigned
        - [ ] better parent layer function after individual file support
    - [x] file for layer mappings
        - [x] list parent layer
            - [ ] use this to sort layer list (children come after their parents)
    - [x] lighting
        - [x] custom lighting color per layer
        - [x] custom lighting pattern for each layer
        - [ ] keys that change layers show those layer colors
        - [ ] if no layer pattern is specified, light the keys that have layer-specific actions
    - [x] implement improved mousekeys as a layer
        - [x] have a function that runs while it's being held?
            - [ ] hold functions increment a counter
- [x] rotary click input
    - [x] have default rotary mode per-layer
    - [x] default: click to enter Layer Select layer
    - [x] default: volume control on rotation
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
- [ ] make a function that will ASCII up a cheat sheet for the layers?
- [ ] count keypresses
- [ ] screen(s)
    - [ ] figure out how to display a progress bar
    - [ ] work on incorporating a pomodoro timer using the time lib
    - [ ] show timer progress
    - [ ] figure out if there's a way to have a log in the serial pane/second OLED without printing to the main screen
    - [ ] find the repo for the little ASCII python pet
        - [ ] see if we can render the cute faces to the OLED
    - [ ] attach second OLED (can those be chained with other STEMMA QT boards?)
- [ ] support for a plover mode?