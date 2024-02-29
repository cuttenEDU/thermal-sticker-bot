from typing import BinaryIO
import io

from PIL import Image,ImageOps



def sticker_to_bw_image(sticker_webp: BinaryIO) -> bytes:
    sticker_image = Image.open(sticker_webp,formats=["WEBP"])

    white_bg = Image.new("RGB",sticker_image.size,(255,255,255))

    if sticker_image.mode == "RGB":
        white_bg.paste(sticker_image,(0,0))
    elif sticker_image.mode == "RGBA":
        white_bg.paste(sticker_image, (0, 0),sticker_image)

    white_bg = ImageOps.grayscale(white_bg)

    white_bg_bytes = io.BytesIO()
    white_bg.save(white_bg_bytes,format="JPEG")
    white_bg_bytes.seek(0)

    return white_bg_bytes.read()