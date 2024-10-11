import fitz


with fitz.open('order.pdf') as pdf_1, fitz.open() as pdf_2, fitz.open('clear.pdf') as pdf_3:
    for i in range(len(pdf_1)):
        pdf_2.insert_pdf(pdf_3, from_page=0, to_page=0)

        type = pdf_1[i].get_text().split()[0].lower().title()
        gender = pdf_1[i].get_text().split()[2]
        colour = pdf_1[i].get_text().split()[9].lower().title()
        size = pdf_1[i].get_text().split()[10]

        pdf_2[i].insert_font(fontname='arial', fontfile='Arial.ttf')
        pdf_2[i].insert_font(fontname='arial-bold', fontfile='Arial-bold.TTF')

        text = '\n\nМатериал верха: Кожа/Текстиль\nМатериал прокладки: Кожа/Текстиль/Мех\nМатериал низа: Полимерный материал\nГарантийный срок: 60 дней'
        pdf_2[i].insert_text((4, 14), f'{type} {gender}\n{colour} {size}', fontname="arial-bold", fontsize=10, color=(0, 0, 0))
        pdf_2[i].insert_text((4, 14), text, fontname="arial", fontsize=9, color=(0, 0, 0))

        # Получаем информацию о первой картинке на странице pdf_1
        images_1 = pdf_1[i].get_images(full=True)

        # Если картинка найдена, получаем ее Xref
        xref_1 = images_1[0][0]  # Xref первой картинки

        # Получаем байты изображения
        base_image = pdf_1.extract_image(xref_1)
        img_bytes = base_image['image']  # Получаем байты изображения

        # Получаем информацию о второй картинке на странице pdf_2
        images_2 = pdf_2[i].get_images(full=True)

        # Если картинка найдена, получаем ее Xref
        xref_2 = images_2[2][0]  # Xref второй картинки
        rect = pdf_2[i].get_image_rects(xref_2)[0]
        pdf_2[i].delete_image(xref_2)

        # Вставляем первую картинку из pdf_1 в pdf_2
        pdf_2[i].insert_image(rect, stream=img_bytes)

    pdf_2.save('final.pdf')
