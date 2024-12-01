# https://pystray.readthedocs.io/en/latest/usage.html
import pystray
from PIL import Image, ImageDraw, ImageFont


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

def create_image_with_text(width, height, color, text='0000'):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color)
    # font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 64)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 750)
    # print(font.get_variation_names())
    # font = ImageFont.FreeTypeFont("Pillow/Tests/fonts/FreeMono.ttf", 64)
    # font.set_variation_by_name('Bold')
    dc = ImageDraw.Draw(image)
    dc.text((0, 0), text, fill='white', font=font)
    return image


# image = create_image_with_text(128, 64, 'white', 'Hello')
# image.show()

# In order for the icon to be displayed, you must provide an icon
icon = pystray.Icon(
    'test name',
    # icon=create_image(64, 64, 'black', 'white'))
    icon=create_image_with_text(2000, 1100, 'black', '0000'))


if __name__ == '__main__':
    # To finally show you icon, call run
    icon.run()

