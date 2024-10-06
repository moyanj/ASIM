from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stdout, level="DEBUG", format="{elapsed} | <level>{level}</> | {message}"
)
