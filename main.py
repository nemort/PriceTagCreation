import fitz


def create(file, bot, chat_id):
    with fitz.open(file) as pdf_1, fitz.open() as pdf_2, fitz.open('clear.pdf') as pdf_3:
        for i in range(len(pdf_1)):
            pdf_2.insert_pdf(pdf_3, from_page=0, to_page=0)

            type = pdf_1[i].get_text().split()[2].lower().title()
            gender = pdf_1[i].get_text().split()[3]
            colour = pdf_1[i].get_text().split()[10].lower().title()
            size = pdf_1[i].get_text().split()[11]

            pdf_2[i].insert_font(fontname='arial', fontfile='Arial.ttf')
            pdf_2[i].insert_font(fontname='arial-bold', fontfile='Arial-bold.TTF')

            text = '\n\nМатериал верха: Кожа/Текстиль\nМатериал прокладки: Кожа/Текстиль/Мех\nМатериал низа: Полимерный материал\nГарантийный срок: 60 дней'
            pdf_2[i].insert_text((4, 14), f'{type} {gender}\n{colour} {size}', fontname="arial-bold", fontsize=10, color=(0, 0, 0))
            pdf_2[i].insert_text((4, 14), text, fontname="arial", fontsize=9, color=(0, 0, 0))

            # Определяем прямоугольник, в котором находится изображение (координаты нужно уточнить)
            search_rect = fitz.Rect(0, 0, 80, 80)  # Координаты исходного изображения

            # Ищем изображение на исходной странице
            image_list = pdf_1[i].get_images(full=True)

            # Цикл по всем изображениям на странице
            for img in image_list:
                # Получаем xref (идентификатор) изображения
                xref = img[0]

                # Получаем bbox (границы изображения)
                img_bbox = pdf_1[i].get_image_rects(xref)[0]

                # Если изображение находится в пределах указанных координат
                if img_bbox.intersects(search_rect):
                    # Извлекаем изображение
                    image = pdf_1.extract_image(xref)
                    image_bytes = image["image"]

                    # Указываем новые координаты для вставки изображения в другой документ
                    dest_rect = fitz.Rect(175, 90, 280, 195)

                    # Вставляем изображение на нужную страницу в целевом документе
                    pdf_2[i].insert_image(dest_rect, stream=image_bytes)

                    break  # Прекращаем цикл, если нашли нужное изображение

            if i % 1000 == 0 and i != 0:
                bot.send_message(chat_id, f"Обработано {i} страниц.")

        pdf_2.save('Ценники.pdf')
