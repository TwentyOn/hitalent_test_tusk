import json
import os
from collections import defaultdict
import shutil
from string import digits

def script1():
    img_path = 'docs/images/train'
    save_path = 'docs/images'

    with open('docs/annotations/instances_train.json') as json_file:
        coco = json.load(json_file)

    id_to_category = {cat['id']: cat['name'] for cat in coco['categories']}

    img_to_classes = defaultdict(set)
    for ann in coco['annotations']:
        img_to_classes[ann['image_id']].add(id_to_category[ann['category_id']])

    for img in coco['images']:
        cls = '_'.join(c.split('_')[0] for c in img_to_classes[img['id']])
        img_name = img['file_name']

        source_path = os.path.join(img_path, img_name)
        target_path = os.path.join(save_path, cls, img_name)

        if cls:
            os.makedirs(os.path.join(save_path, cls), exist_ok=True)
            shutil.move(source_path, target_path)


if __name__ == '__main__':
    script1()