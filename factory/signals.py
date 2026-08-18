"""
Django signals for the factory app.
Auto-converts uploaded videos to H.264 for browser compatibility.
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FactoryVideo
from .video_utils import convert_video_to_h264

logger = logging.getLogger(__name__)


@receiver(post_save, sender=FactoryVideo)
def convert_factory_video_on_save(sender, instance, **kwargs):
    """
    After a FactoryVideo is saved, convert the video_file to H.264 MP4
    so it plays correctly in all browsers (including Chrome on Windows
    which does not support H.265/HEVC from WhatsApp videos).
    """
    if not instance.video_file:
        return

    try:
        file_path = instance.video_file.path
        logger.info(f"[factory.signals] Converting video to H.264: {file_path}")
        success = convert_video_to_h264(file_path)
        if success:
            logger.info(f"[factory.signals] Video successfully converted: {file_path}")
        else:
            logger.warning(f"[factory.signals] Video conversion failed or skipped: {file_path}")
    except Exception as e:
        logger.error(f"[factory.signals] Error during video conversion: {e}")
