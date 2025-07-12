from celery import shared_task
from PIL import Image
import os

@shared_task
def resize_avatar(path, size=(300, 300)):
    try:
        img = Image.open(path)
        img = img.convert("RGB")
        img.thumbnail(size)
        img.save(path)
    except Exception as e:
        print("Error resizing avatar:", e)
