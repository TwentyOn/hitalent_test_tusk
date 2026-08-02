import json
import os
from collections import defaultdict
from string import digits, punctuation
import shutil

from settings import COCO_FILE_PATH, IMG_PATH, OUTPUT_PATH, UPDATE_ANN_PATH

def script1():
    with open(COCO_FILE_PATH) as coco_json_file:
        coco = json.load(coco_json_file)

    id_to_category = {cat['id']: cat['name'] for cat in coco['categories']}

    img_to_classes = defaultdict(set)
    for ann in coco['annotations']:
        clean_class = id_to_category[ann['category_id']].strip(digits+punctuation)
        img_to_classes[ann['image_id']].add(clean_class)

    for img in coco['images']:
        cls = '_'.join(c.split('_')[0] for c in img_to_classes[img['id']])
        img_name = img['file_name']
        source_path = IMG_PATH / img_name
        target_path = OUTPUT_PATH / 'images' / cls / img_name
        img['file_name'] = target_path.as_posix()
        os.makedirs(os.path.join(OUTPUT_PATH / 'images', cls), exist_ok=True)
        shutil.copy(source_path, target_path)

    if not os.path.exists(UPDATE_ANN_PATH):
        os.makedirs(UPDATE_ANN_PATH.parent, exist_ok=True)
    with open(UPDATE_ANN_PATH, 'w') as upd_ann_json_file:
        json.dump(coco, upd_ann_json_file, indent=4)


if __name__ == '__main__':
    script1()
