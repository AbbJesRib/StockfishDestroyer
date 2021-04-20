from PIL import Image
# import os

# for filename in os.listdir(directory):
#     if filename.endswith(".asm") or filename.endswith(".py"):
#          # print(os.path.join(directory, filename))
#         continue
#     else:
#         continue
opacity_level = 170

img = Image.open('./pieces/blackBishopcopy.png')
img.convert('RGBA')

img.putalpha(opacity_level)


img.save('./pieces/alphablackBishopcopy.png', format='png')