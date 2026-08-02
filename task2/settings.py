import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s  - %(levelname)s - %(message)s')

BASE_DIR = Path(__file__).parent
COCO_FILE_PATH = BASE_DIR / 'docs/annotations/instances_train.json'
IMG_PATH = BASE_DIR / 'docs/images/train'
OUTPUT_PATH = BASE_DIR / 'output'
UPDATE_ANN_PATH = BASE_DIR / OUTPUT_PATH / 'annotations/updated_annotations.json'