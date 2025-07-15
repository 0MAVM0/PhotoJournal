from celery import shared_task
from PIL import Image


@shared_task
def resize_avatar(path: str, size: tuple = (300, 300)) -> None:
    try:
        img = Image.open(path)
        img = img.convert("RGB")
        img.thumbnail(size)
        img.save(path)
    except Exception as e:
        print("Error resizing avatar:", e)
