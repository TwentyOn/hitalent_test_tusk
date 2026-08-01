import json
import os
from pathlib import Path
from collections import defaultdict
import shutil

IMG_PATH = Path('docs/images/train')
SAVE_PATH = Path('docs/images')
COCO_FILE_PATH = Path('docs/annotations/instances_train.json')

def script1():
    with open(COCO_FILE_PATH) as coco_json_file:
        coco = json.load(coco_json_file)

    id_to_category = {cat['id']: cat['name'] for cat in coco['categories']}

    img_to_classes = defaultdict(set)
    for ann in coco['annotations']:
        img_to_classes[ann['image_id']].add(id_to_category[ann['category_id']])

    for img in coco['images']:
        cls = '_'.join(c.split('_')[0] for c in img_to_classes[img['id']])
        img_name = img['file_name']
        source_path = IMG_PATH / img_name
        target_path = SAVE_PATH / cls / img_name
        img['file_name'] = target_path.as_posix()
        os.makedirs(os.path.join(SAVE_PATH, cls), exist_ok=True)
        shutil.move(source_path, target_path)

    update_ann_path = COCO_FILE_PATH.parent / 'updated_annotations.json'
    with open(update_ann_path, 'w') as upd_ann_json_file:
        json.dump(coco, upd_ann_json_file, indent=4)


if __name__ == '__main__':
    script1()
