# https://pystray.readthedocs.io/en/latest/usage.html
import os

import pystray
import Xlib.error
import Xlib.Xutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Pillow 10+ removed Image.ANTIALIAS; pystray still references it.
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# NOTE: it must remove these packages else the backend `xorg` doesn't work: pip uninstall pycairo PyGObject
os.environ["PYSTRAY_BACKEND"] = "xorg"

# NOTE: it must install these packages to work with below backends: pip install pycairo PyGObject
# NOTE: In these backends, the icon is larger
# os.environ['PYSTRAY_BACKEND'] = 'appindicator'
# os.environ["PYSTRAY_BACKEND"] = "gtk"


def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

# Solid colour of the GNOME panel behind the tray, sampled from a screenshot.
# The icon is painted opaque with this colour (not left transparent) so the tray
# window's own near-black background never shows as a dark ring around the text.
PANEL_BG = (19, 19, 19)
# Tray slot height on this panel; rendering the label at exactly this height lets
# the backend paste it 1:1 instead of LANCZOS-resizing (whose edge undershoot is
# what produced the thin black outline around the white glyphs).
SLOT_H = 34


def create_image_with_text(width, height, color, text='0000'):
    # Goal: white digits that look exactly like the GNOME panel clock next to the
    # tray - pure white, no dark outline, thin strokes - readable at ~34px tall.
    #
    # Why it is done THIS way (do not "simplify" back to a plain RGBA icon, it
    # brings the black outline back):
    #   1. The tray window's own background is near-black (~1,1,1), which is
    #      DARKER than the panel (~19,19,19). A transparent/RGBA icon lets that
    #      near-black show around the glyphs -> looks like a black outline.
    #      Fix: paint the icon OPAQUE with the panel colour PANEL_BG.
    #   2. The backend LANCZOS-resizes the icon to the slot; LANCZOS undershoots
    #      at sharp white/dark edges, dipping BELOW the background toward black
    #      -> a thin dark ring. Fix: resize a grayscale MASK, then composite
    #      white over PANEL_BG. The composite floor is PANEL_BG, so nothing can
    #      ever end up darker than the panel. Also render at SLOT_H so the
    #      backend paste is ~1:1 and barely resizes.
    #   3. _WideIcon widens the tray slot to this label's aspect ratio so
    #      multi-digit numbers stay separated instead of squashed into ~24px.
    # Stroke weight is tuned with the MinFilter erosion below (smaller kernel =
    # thicker strokes); Ubuntu Light is already the thinnest sensible base.
    font_path = "/usr/share/fonts/truetype/ubuntu/Ubuntu-L.ttf"
    font = ImageFont.truetype(font_path, 300)
    measure = ImageDraw.Draw(Image.new('L', (1, 1)))
    bbox = measure.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    hpad, vpad = 30, 20
    big_w, big_h = text_w + 2 * hpad, text_h + 2 * vpad
    mask = Image.new('L', (big_w, big_h), 0)
    ImageDraw.Draw(mask).text((hpad - bbox[0], vpad - bbox[1]), text, fill=255, font=font)
    # Stroke weight = full Ubuntu Light (no erosion). Add ImageFilter.MinFilter(3)
    # here to shave ~1px/side thinner, or MaxFilter(3) to fatten ~1px/side.
    final_w = max(1, round(big_w * SLOT_H / big_h))
    mask = mask.resize((final_w, SLOT_H), Image.LANCZOS)
    image = Image.composite(
        Image.new('RGB', (final_w, SLOT_H), (255, 255, 255)),
        Image.new('RGB', (final_w, SLOT_H), PANEL_BG),
        mask,
    )
    print("create_image_with_text", text)
    return image


class _WideIcon(pystray.Icon):
    """Tray icon that resizes its slot to match the icon's aspect ratio.

    The XEmbed tray hands out a ~24px-wide square by default, which crushes
    multi-digit numbers into an unreadable blob. Overriding the xorg backend's
    _draw lets us widen the window to fit the current image before painting.
    """

    def _draw(self):
        try:
            dim = self._window.get_geometry()
            h = dim.height or 24
            img = self._icon
            want_w = max(24, round(h * img.width / img.height))
            if dim.width != want_w:
                # The tray honours min_width, so pin it to keep the wider slot;
                # a bare configure() gets shrunk back to the 24px minimum.
                self._window.set_wm_normal_hints(
                    flags=(Xlib.Xutil.PMinSize | Xlib.Xutil.PSize),
                    min_width=want_w,
                    min_height=h,
                )
                self._window.configure(width=want_w, height=h)
                self._display.sync()
                dim = self._window.get_geometry()
            self._assert_icon_data(dim.width, dim.height)
            self._window.put_pil_image(self._gc, 0, 0, self._icon_data)
        except Xlib.error.BadDrawable:
            # The window has been destroyed; ignore
            pass


# image = create_image_with_text(128, 64, 'white', 'Hello')
# image.show()

# In order for the icon to be displayed, you must provide an icon
icon = _WideIcon(
    'test name',
    # icon=create_image(200, 200, 'black', 'white'))
    icon=create_image_with_text(2000, 1000, "black", "1234"),
)


if __name__ == '__main__':
    # To finally show you icon, call run
    icon.run()
    # icon.run_detached()
