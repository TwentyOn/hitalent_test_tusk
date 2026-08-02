import json
import os
import shutil
from pathlib import Path
from collections import defaultdict

from task2.settings import logger, UPDATE_ANN_PATH, COCO_FILE_PATH, OUTPUT_PATH, IMG_PATH


def convert_coco_to_yolo_with_images(coco_json_path: str, output_dir: str, images_base_dir: str='.'):
    with open(coco_json_path, 'r', encoding='utf-8') as f:
        coco_data = json.load(f)

    category_map = {}
    for idx, cat in enumerate(coco_data['categories']):
        category_map[cat['id']] = {
            'yolo_id': idx,
            'name': cat['name']
        }

    images_dict = {}
    for img in coco_data['images']:
        images_dict[img['id']] = {
            'file_name': img['file_name'],
            'width': img['width'],
            'height': img['height']
        }

    annotations_by_image = defaultdict(list)
    for ann in coco_data['annotations']:
        annotations_by_image[ann['image_id']].append(ann)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for image_id, annotations in annotations_by_image.items():
        if image_id not in images_dict:
            continue

        img_info = images_dict[image_id]
        img_width = img_info['width']
        img_height = img_info['height']

        file_path = img_info['file_name']
        file_name = Path(file_path).stem
        file_full_name = Path(file_path).name

        categories_in_image = set()
        for ann in annotations:
            if ann['category_id'] in category_map:
                categories_in_image.add(category_map[ann['category_id']]['name'])

        if len(categories_in_image) > 1:
            folder_name = '_'.join(sorted(categories_in_image))
        else:
            folder_name = list(categories_in_image)[0] if categories_in_image else 'unknown'

        yolo_folder = output_path / folder_name
        yolo_folder.mkdir(parents=True, exist_ok=True)

        src_image_path = None

        possible_paths = [
            Path(images_base_dir) / file_path,
            Path(images_base_dir) / file_full_name,
            Path(images_base_dir) / Path(file_path).parent.name / file_full_name,
        ]

        possible_parents = ['docs/images', 'docs/images/aalst', 'docs/images/playhood',
                            'docs/images/club21', 'docs/images/lazada', 'docs/images/singtel',
                            'docs/images/klarra', 'docs/images/m1', 'docs/images/something']

        for parent in possible_parents:
            possible_paths.append(Path(images_base_dir) / parent / file_full_name)

        for path in possible_paths:
            if path.exists():
                src_image_path = path
                break

        if src_image_path:
            dst_ext = src_image_path.suffix if src_image_path.suffix else '.jpg'
            dst_image_path = yolo_folder / f"{file_name}{dst_ext}"

            shutil.copy2(src_image_path, dst_image_path)
        else:
            logger.warning(f"Изображение не найдено для {file_path}")
            continue

        yolo_txt_path = yolo_folder / f"{file_name}.txt"

        with open(yolo_txt_path, 'w', encoding='utf-8') as yolo_file:
            for ann in annotations:
                if ann['category_id'] not in category_map:
                    continue

                class_id = category_map[ann['category_id']]['yolo_id']

                x, y, width, height = ann['bbox']

                x_center = (x + width / 2) / img_width
                y_center = (y + height / 2) / img_height
                norm_width = width / img_width
                norm_height = height / img_height

                yolo_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}\n")
        logger.info(f'YOLO-аннотации созданы: {yolo_folder}')




def main():
    output_dir = OUTPUT_PATH / 'yolo_dataset'
    images_base_dir = IMG_PATH

    if not os.path.exists(UPDATE_ANN_PATH):
        logger.error(f"Файл {UPDATE_ANN_PATH} не найден!")
        return

    convert_coco_to_yolo_with_images(COCO_FILE_PATH, output_dir, images_base_dir)


if __name__ == "__main__":
    main()