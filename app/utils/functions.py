import asyncio
from typing import List, Dict
from PIL.ImageDraw import ImageDraw
from PIL import Image, ImageDraw, ImageFont


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
            f"/Users/matvei/PycharmProjects/PythonProject/app/src/part_{k}_{v}.png"
        ).convert("RGBA")

        merged_img.paste(img, (x, y), img)

        if k % 3 == 0:
            y += img.size[1]
            x = 0
            continue

        x += img.size[0]

    # ===== ШРИФТ =====
    font_path = "/Users/matvei/PycharmProjects/PythonProject/app/fonts/helvetica_bold.otf"

    font_text_1 = ImageFont.truetype(font_path, 42)  # письмо
    font_text_2 = ImageFont.truetype(font_path, 48)  # имя

    # ===== ПИСЬМО — БЕЗ ЦЕНТРИРОВАНИЯ =====
    def draw_letter_text(base_img, text, position, size, angle, font):
        text_layer = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_layer)

        # рисуем от левого верхнего угла
        draw.text((0, 0), text, font=font, fill=(0, 0, 0, 255))

        rotated = text_layer.rotate(angle, expand=True)
        base_img.paste(rotated, position, rotated)

    # ===== ИМЯ — ЦЕНТР ТОЛЬКО ПО ГОРИЗОНТАЛИ =====
    def draw_name_text(base_img, text, position, size, angle, font):
        text_layer = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_layer)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]

        text_x = (size[0] - text_width) // 2
        text_y = 0

        draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0, 255))

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
        f"/Users/matvei/PycharmProjects/PythonProject/users_report/{name_report}.png"
    )

asyncio.run(create_report({1: '2', 2: '2', 3: 1, 4: '3', 5: 1, 6: '1', 7: '2', 8: '2', 9: '2'},
                          text_1="123123123",
                          text_2="123123123",
                          name_report="report",))