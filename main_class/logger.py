import logging


logging.basicConfig(level = logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler('file.log'),logging.StreamHandler()])


verge_logger = logging.getLogger(__name__)