import json
import os
import logging

from script1 import COCO_FILE_PATH

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s  - %(levelname)s - %(message)s')


def script2():
    with open(COCO_FILE_PATH.parent / 'updated_annotations.json') as f:
        coco_data = json.load(f)

    miss_imgs = []
    for img in coco_data['images']:
        filename = img['file_name']
        if not os.path.exists(filename):
            miss_imgs.append(filename)
            logger.warning('несуществующий файл:', filename)
    else:
        logger.info('все файлы на месте')

    ann_img_ids = {ann['id'] for ann in coco_data['annotations']}
    img_ids = {img['id'] for img in coco_data['images']}
    miss_img_ids = ann_img_ids.difference(img_ids)
    if miss_img_ids:
        logger.warning(
            f'Изображения отсутствуют в аннотациях или списке изоборажений (ID): {ann_img_ids.difference(img_ids)}')

    ann_cat_ids = {ann['category_id'] for ann in coco_data['annotations']}
    cat_ids = {cat['id'] for cat in coco_data['categories']}
    miss_cat_ids = cat_ids.difference(ann_cat_ids)
    if miss_cat_ids:
        logger.warning(f'Категории отсутствуют в аннотациях или списке категорий (ID): {miss_cat_ids}')

    error_cnt = len(miss_cat_ids) + len(miss_img_ids)
    path_error_cnt = len(miss_imgs)
    ids_img_error_cnt = len(miss_img_ids)
    ids_cat_error_cnt = len(miss_cat_ids)
    img_cnt = len(coco_data['images'])
    ann_cnt = len(coco_data['annotations'])

    logger.info(f'Ошибок: {error_cnt}')
    logger.info(f'Ошибки путей файлов: {path_error_cnt}')
    logger.info(f'Ошибки соглассованости аннотации/список изображений: {ids_img_error_cnt}')
    logger.info(f'Ошибки соглассованости аннотации/список категорий: {ids_cat_error_cnt}')
    logger.info(f'Количество изображений: {img_cnt}')
    logger.info(f'Количество аннотаций: {ann_cnt}')

    with open('dataset_report.json', 'w') as json_file:
        data = {
            'error_count': error_cnt,
            'path_errors': {
                'count': path_error_cnt,
                'files': miss_imgs,
            },
            'annotation_errors': {
                'image_annotations': {
                    'count': ids_img_error_cnt,
                    'missing_ids': sorted(list(miss_img_ids)),
                },
                'categories_annotations': {
                    'count': ids_cat_error_cnt,
                    'missing_ids': sorted(list(miss_cat_ids)),
                },
            },
            'images_count': img_cnt,
            'annotations_count': ann_cnt,
        }
        json.dump(data, json_file, indent=4)


if __name__ == '__main__':
    script2()
