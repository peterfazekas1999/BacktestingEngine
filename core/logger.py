import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # or DEBUG for more detail

# Only add handlers if they don't already exist (avoid duplicate logs)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
