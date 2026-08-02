import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s  - %(levelname)s - %(message)s')

BASE_DIR = Path(__file__).parent