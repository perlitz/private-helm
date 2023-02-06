from typing import List
import os

from .watermark_detector import WatermarkDetector


def test_compute_watermark_probability():
    watermark_detector = WatermarkDetector()

    # These test images are from https://github.com/LAION-AI/LAION-5B-WatermarkDetection
    base_path = os.path.dirname(__file__)
    clear_image_path: str = os.path.join(base_path, "test_images", "clear_example.png")
    watermark_image_path: str = os.path.join(base_path, "test_images", "watermark_example.png")

    has_watermarks: List[bool] = watermark_detector.has_watermark([clear_image_path, watermark_image_path])[0]
    assert has_watermarks == [False, True]
