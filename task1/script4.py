import os
from xml.etree import ElementTree

from script1 import files

def script4():
    write_path = 'docs/{}_modified.xml'

    for file in files:
        tree = ElementTree.parse(file)
        root = tree.getroot()

        images = root.findall('image')
        length = len(images)

        for i in range(length // 2):
            img1, img2 = images[i], images[length - i - 1]
            name1, name2 = img1.attrib['name'], img2.attrib['name']

            img1.attrib['id'], img2.attrib['id'] = img2.attrib['id'], img1.attrib['id']
            img1.attrib['name'] = f'{name1.split('/')[-1][:-4]}.png'
            img2.attrib['name'] = f'{name2.split('/')[-1][:-4]}.png'

        tree.write(write_path.format(file.split(os.sep)[-1][:-4]), encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    script4()