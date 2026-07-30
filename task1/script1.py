import os
from xml.etree import ElementTree

FIGURE_TAGS = ['box', 'polygon', 'points']
files = [file.path for file in os.scandir('docs') if file.path.endswith('.xml')]

def figure_exist(image):
    return any(image.find(tag) is not None for tag in FIGURE_TAGS)


def script1():
    image_count = 0
    marked_image_count = 0
    figure_count = 0
    max_size = [0.0, 0.0, '', 0]
    min_size = [float('-inf'), float('-inf'), '', 0]

    figures = []

    for file in files:
        tree = ElementTree.parse(file)
        root = tree.getroot()


        for image in root.iter(tag='image'):
            image_count += 1

            width = float(image.attrib['width'])
            height = float(image.attrib['height'])

            if max_size[0] * max_size[1] < width * height:
                max_size[0] = width
                max_size[1] = height
                max_size[2] = image.attrib['name']
                max_size[3] += 1

            if min_size[0] * min_size[1] > width * height:
                min_size[0] = width
                min_size[1] = height
                min_size[2] = image.attrib['name']
                min_size[3] += 1

            if figure_exist(image):
                marked_image_count += 1

                for tag in FIGURE_TAGS:
                    figs = image.findall(tag)
                    figures.extend(figs)
                    figure_count += len(figs)

    if __name__ == '__main__':
        print('Общее количество изображений: ', image_count)
        print('Количество размеченных изображений:', marked_image_count)
        print('Количество неразмеченных изображений:', image_count - marked_image_count)
        print('Количество фигур на всех изображениях:', figure_count)
        print(f'Самое большое изображение:',
              max_size if max_size[3] <= 1 else max_size[0], max_size[1], f'({max_size[3]} шт.)')
        print('Самое маленькое изображение:',
              min_size if min_size[3] <= 1 else min_size[0], min_size[1], f'({min_size[3]} шт.)')

    return figures

if __name__ == '__main__':
    script1()