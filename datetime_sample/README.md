# time_rest.py - testing

## Run an isolated test instance

```bash
datetime_sample/test.sh        # working time 70s: 20s white, 50s blinking, then warning
datetime_sample/test.sh 120    # custom working time in seconds
```

It runs next to the real instance without touching it. Quit it from its own (second) tray icon.

`test.sh` sets these env vars (all unset = normal behaviour):

| Env var | Effect |
|---|---|
| `TIME_REST_INSTANCE=test` | log to `/tmp/time_rest_test.log`, feh window title `test-warning` |
| `TIME_REST_WORK_SECONDS=70` | working time in seconds (default `20 * 60`) |
| `TIME_REST_NO_LOCK=1` | `lock_screen()` only prints, never locks |

Do not start or even `import time_rest` without `TIME_REST_INSTANCE`: it opens
`/tmp/time_rest.log` with `"w"` and wipes the real instance's log.

## Expected result

- Working time: label white, then red/white every second during the last 50s.
- Warning phase (feh image cycle): label `!` blinking red/white.
- Pause: label `II`, no blinking.

## Screenshot the system tray (check font / colour)

```bash
# 1. Find the tray icons (pystray xorg windows): last column = absolute x,y on screen
xwininfo -root -tree | grep SystemTrayIcon
#   ... ("test nameSystemTrayIcon" "test name")  77x34+0+0  +1746+1080

# 2. Crop the panel strip around that point (WxH+X+Y), then open the PNG
mkdir -p tmp && import -window root -crop 1000x36+1300+1079 tmp/tray.png
```

Take a few shots 0.5s apart to catch both colours, and pair each with
`tail -1 /tmp/time_rest_test.log` to know which second it shows.
