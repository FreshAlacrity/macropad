# Macropad
CircuitPython for [Adafruit MacroPad RP2040](https://www.adafruit.com/product/5128)

## Design Concepts
tamtam in the keyboard is a pet we take care of when we take care of ourselves/a nudge to be more routine about self care, so it needs breaks from taking input and to be fed and watered and get enough sleep, and it'll cheerfully turn down the lights or refuse to take input if it needs a break
  - takes breaks only after sensible inputs (ESC, CTRL+S) when there's been ~25 minutes of activity recently
    - snooze function for wrapping up tasks
  - squeaks indignantly if you keep trying to use it during a break

## References
- to list modules: `help("modules")`
- `dir(board)` after `import(board)` lists all the pins available
- https://circuitpython.org/libraries
- https://learn.adafruit.com/ir-sensor
- https://circuitpython.readthedocs.io/projects/bundle/en/latest/drivers.html
- https://learn.adafruit.com/circuitpython-display-support-using-displayio/tilegrid-and-group
- https://adafruit-circuitpython-bitmap-saver.readthedocs.io/en/latest/api.html
- https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/usb-setup-timing
- https://github.com/kmatch98/CircuitPython_memory_saving
- https://learn.adafruit.com/welcome-to-circuitpython/frequently-asked-questions#memory-issues-3129414
- https://learn.adafruit.com/Memory-saving-tips-for-CircuitPython?view=all
- https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices#composite-hid-devices-3096611
- https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices
- https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/overview
- https://docs.circuitpython.org/projects/bitmapsaver/en/latest/api.html
- https://github.com/adafruit/Adafruit_CircuitPython_ProgressBar/tree/main/examples
- https://docs.circuitpython.org/en/latest/shared-bindings/watchdog/index.html
- https://learn.adafruit.com/circuitpython-display-support-using-displayio/sprite-sheet
- https://learn.adafruit.com/circuitpython-display-support-using-displayio/ui-quickstart#groups-3033357
- https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio
- https://learn.adafruit.com/macropad-hotkeys/custom-configurations
- https://docs.circuitpython.org/projects/macropad/en/latest/api.html
- https://docs.circuitpython.org/projects/hid/en/latest/
- https://docs.circuitpython.org/projects/hid/en/latest/examples.html#simple-gamepad
- https://docs.circuitpython.org/projects/display-shapes/en/latest/api.html#adafruit_display_shapes.rect.Rect
- https://learn.adafruit.com/adafruit-macropad-rp2040/
- [All supported keycodes](https://usb.org/sites/default/files/hut1_21_0.pdf#page=83)
  - note that keycodes are the names for key *positions* on a US keyboard
- [Guide for setting up external displays](https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus)

### Possible Fonts
- terminalio 
    - fast but sadly not many special characters
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

## Key Action Types
Action specific layer-maps

Called on release, if False default back to above action:
.  tap: if released quickly
.. tap-tap: overrides regular tap behavior after a tap
-. hold-tap: overrides regular tap behavior after a hold
-  hold: if not released quickly
.- tap-hold: overrides regular hold behavior immediately after a tap
-- hold-hold: overrides regular hold behavior immediately after a hold

Called on key press/while held:
^  immediate: when pressed
=  input: constant + immediate input while being held (for opening layers and game input)

## To Do
- refactor to support all key actions listed above
- add aliases for l_tab l_shift r_shift etc
- Goal: Replace the Mouse
  - [ ] desired behavior: if the last action was holding the same key, resume hold (otherwise immediately do the tap action)
  - [ ] rotary inherits last directional action
  - [ ] toggle scroll mode for mouse movement (hold middle click)
  - [ ] actions to increase and decrease cursor speed
  - [ ] Layer specific mouse speed support
    - [ ] Minecraft layer for inventory view with mouse speed so a tap moves one inventory square
- Refactoring
  - [ ] generic hold-key actions (for arrow keys etc)
- [ ] Figure out that watchdog thing that reboots it when it crashes
- consolidate and prioritize Later todos

### Later
- Goal: Custom T9 Style Input
  - [ ] track inputs, combining precise and #char inputs, including previous words (for prediction and also backspace to fix)
  - [ ] inputs:
    - [ ] 9 or so character input keys
      - [ ] show predicted words on OLED while entering T9 style
      - [ ] make a dictionary and assign letters to keys based on keylogger info
    - [ ] next/space key: pressing again after an initial press swaps in the next word in the dictionary, pressing after precise input verifies (shows on OLED) and then adds word to dictionary
    - [ ] back key: deletes the prior character (then the prior word if double tapped quickly and prior input is T9 or character input?)
    - [ ] chords for precise input: hold a character key and then tap another key to select a specific character (release after hold does nothing)
      - [ ] show map of available characters on OLED
  - [ ] 'next key' - immediate action on press (add space, or if space was last input then select next word in dictionary and add space); if previous input wasn't T9 keys, verify (tap again) and add the word to dictionary
- Goal: Pomodoro Timer
  - [ ] get it running for X minutes
  - [ ] beep when the timer ends
  - [ ] run the bar with inverted colors (black bar on white) for breaks
- [ ] key + rotary actions
    - [ ] CTRL > CTRL to center the mouse
    - [ ] undo/redo
    - [ ] Discord hotkeys
    - [ ] cut/copy/paste/select-all
    - macro actions
        - [ ] save: "CTRL + S"
        - [ ] command palette for VSCode: "CTRL + SHIFT + P"
        - [ ] change audio in/out with FxSound key combinations
    - [ ] increase and decrease brightness
    - [ ] alias numbers, i.e.  1 or "1" to "one"
- [ ] Settings file (read and when in write mode, write as updated for things like mouse speed and current layer)
- [ ] Track recent wpm
- [ ] Track layer history
- Refactoring
    - [ ] separate the sprite-sheet-making code into a different file
        - [ ] make and test using sprite sheets for:
            - [ ] layer names
            - [ ] tam tam faces
- [ ] figure out why the framerate is irregular
    - [ ] figure out why making tamtam faces takes so long
- [ ] clean up multi-line comment examples
- [ ] have the backup and commit shortcut also close the explorer window
- [x] get the screen rotated 90 degrees
- [x] add a way to include descriptions of key actions
- [x] make a global value to track mouse movement
    - [ ] add a specialized gaming-mouse layer where it accelerates over a bit of time and then decelerates over a bit of time for viewer comfort
        - [ ] add a per-layer mouse speed modifier
        - [ ] try damped harmonic oscillator mouse movement where it gently eases back a bit after the key is released
    - [ ] mouse_angular_move(theta) that calls mouse_move(cos(theta), sin(theta))
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
    - [ ] see https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices#composite-hid-devices-3096611
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