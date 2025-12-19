import asyncio
from typing import List, Dict
from PIL.ImageDraw import ImageDraw
from PIL import Image, ImageDraw, ImageFont
from decouple import config as env_config

async def create_report(
        answers: Dict[int, str],
        text_1: str,
        text_2: str,
        name_report: str
):
    # ===== ОСНОВНОЕ ИЗОБРАЖЕНИЕ =====
    x, y = 0, 0
    merged_img = Image.new("RGB", (2307, 3076), color="white")

    # ===== СКЛЕЙКА КАРТИНОК =====
    for k, v in answers.items():
        img = Image.open(
            env_config("GLOBAL_PATH") + f"app/src/part_{k}_{v}.png"
        ).convert("RGBA")

        merged_img.paste(img, (x, y), img)

        if k % 3 == 0:
            y += img.size[1]
            x = 0
            continue

        x += img.size[0]

    # ===== ШРИФТ =====
    font_path = env_config("GLOBAL_PATH") + "app/fonts/helvetica_bold.otf"

    font_text_1 = ImageFont.truetype(font_path, 42)  # письмо
    font_text_2 = ImageFont.truetype(font_path, 48)  # имя

    # ===== ПЕРЕНОС ТЕКСТА ПО ШИРИНЕ =====
    def wrap_text(text, font, max_width, draw):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            w = draw.textbbox((0, 0), test_line, font=font)[2]

            if w <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    # ===== ПИСЬМО (С ПЕРЕНОСОМ) =====
    def draw_letter_text(base_img, text, position, size, angle, font):
        text_layer = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_layer)

        lines = wrap_text(text, font, size[0], draw)

        y_offset = 0
        line_height = draw.textbbox((0, 0), "Ay", font=font)[3]

        for line in lines:
            draw.text((0, y_offset), line, font=font, fill=(0, 0, 0, 255))
            y_offset += line_height

        rotated = text_layer.rotate(angle, expand=True)
        base_img.paste(rotated, position, rotated)

    # ===== ИМЯ (С ПЕРЕНОСОМ + ЦЕНТР ПО X) =====
    def draw_name_text(base_img, text, position, size, angle, font):
        text_layer = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_layer)

        lines = wrap_text(text, font, size[0], draw)

        y_offset = 0
        line_height = draw.textbbox((0, 0), "Ay", font=font)[3]

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]

            x = (size[0] - line_width) // 2
            draw.text((x, y_offset), line, font=font, fill=(0, 0, 0, 255))
            y_offset += line_height

        rotated = text_layer.rotate(angle, expand=True)
        base_img.paste(rotated, position, rotated)

    # ===== TEXT 1 — ПИСЬМО =====
    draw_letter_text(
        base_img=merged_img,
        text=text_1,
        position=(1669, 545),
        size=(289, int(259.5)),
        angle=-14.79,
        font=font_text_1
    )

    # ===== TEXT 2 — ИМЯ ДРУГА =====
    draw_name_text(
        base_img=merged_img,
        text=text_2,
        position=(841, 1067),
        size=(432, 142),
        angle=-14.76,
        font=font_text_2
    )

    # ===== СОХРАНЕНИЕ =====
    merged_img.save(
        env_config("GLOBAL_PATH") + f"users_report/{name_report}.png"
    )

# asyncio.run(create_report({1: '2', 2: '2', 3: 1, 4: '3', 5: 1, 6: '1', 7: '2', 8: '2', 9: '2'},
#                           text_1="1234563213 213 289 123456789 123456789 12345678",
#                           text_2="123123123",
#                           name_report="report",))