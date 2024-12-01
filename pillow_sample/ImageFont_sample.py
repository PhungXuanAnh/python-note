from PIL import Image, ImageDraw, ImageFont

image = Image.new('RGB', (1024, 1080), 'white')

draw = ImageDraw.Draw(image)

# use a bitmap font
# font = ImageFont.load("arial.pil")

# draw.text((10, 10), "hello", font=font)

# use a truetype font
font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 15)

# NOTE: there are many truetype fonts in this folder: /usr/share/fonts/truetype
draw.text((10, 25), "world", font=font)
image.show()