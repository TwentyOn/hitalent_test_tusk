import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s  - %(levelname)s - %(message)s')

COCO_FILE_PATH = Path('docs/annotations/instances_train.json')
IMG_PATH = Path('docs/images/train')
OUTPUT_PATH = Path('output')
UPDATE_ANN_PATH = OUTPUT_PATH / 'annotations/updated_annotations.json'
