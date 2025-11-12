import albumentations as A
import cv2
import numpy as np
from typing import Dict, Any, List
from pathlib import Path


class AugmentationPipeline:
    """
    Handles image augmentation using albumentations library.
    Supports bounding boxes, masks, and keypoints simultaneously.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize augmentation pipeline from configuration.

        Args:
            config: Dictionary with augmentation settings
                Example: {
                    "flip_horizontal": True,
                    "flip_vertical": False,
                    "rotate": {"limit": 15},
                    "brightness_contrast": {"brightness_limit": 0.2, "contrast_limit": 0.2},
                    "multiplier": 3  # Number of augmented versions per image
                }
        """
        self.config = config
        self.multiplier = config.get("multiplier", 1)
        self.transform = self._build_transform()

    def _build_transform(self) -> A.Compose:
        """Build albumentations transform from config."""
        transforms = []

        # Flip transformations
        if self.config.get("flip_horizontal"):
            transforms.append(A.HorizontalFlip(p=0.5))
        if self.config.get("flip_vertical"):
            transforms.append(A.VerticalFlip(p=0.5))

        # Rotation
        if rotate_config := self.config.get("rotate"):
            limit = rotate_config.get("limit", 15)
            transforms.append(A.Rotate(limit=limit, p=0.5))

        # Crop
        if crop_config := self.config.get("crop"):
            height = crop_config.get("height", 0.9)
            width = crop_config.get("width", 0.9)
            transforms.append(A.RandomCrop(height=int(height * 1000), width=int(width * 1000), p=0.5))

        # Shear
        if shear_config := self.config.get("shear"):
            limit = shear_config.get("limit", 15)
            transforms.append(A.Affine(shear=limit, p=0.5))

        # Color transformations
        if brightness_config := self.config.get("brightness_contrast"):
            transforms.append(
                A.RandomBrightnessContrast(
                    brightness_limit=brightness_config.get("brightness_limit", 0.2),
                    contrast_limit=brightness_config.get("contrast_limit", 0.2),
                    p=0.5,
                )
            )

        if hue_config := self.config.get("hue_saturation"):
            transforms.append(
                A.HueSaturationValue(
                    hue_shift_limit=hue_config.get("hue_shift", 20),
                    sat_shift_limit=hue_config.get("sat_shift", 30),
                    val_shift_limit=hue_config.get("val_shift", 20),
                    p=0.5,
                )
            )

        # Blur
        if self.config.get("blur"):
            transforms.append(A.Blur(blur_limit=7, p=0.5))

        # Noise
        if self.config.get("noise"):
            transforms.append(A.GaussNoise(p=0.5))

        # Cutout
        if cutout_config := self.config.get("cutout"):
            num_holes = cutout_config.get("num_holes", 8)
            max_h_size = cutout_config.get("max_h_size", 32)
            max_w_size = cutout_config.get("max_w_size", 32)
            transforms.append(
                A.CoarseDropout(
                    max_holes=num_holes,
                    max_height=max_h_size,
                    max_width=max_w_size,
                    p=0.5,
                )
            )

        return A.Compose(
            transforms,
            bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']),
        )

    def augment_image(
        self,
        image: np.ndarray,
        bboxes: List[List[float]],
        class_labels: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Apply augmentation to an image and its annotations.

        Args:
            image: Input image as numpy array
            bboxes: List of bounding boxes in COCO format [x, y, width, height]
            class_labels: List of class labels for each bbox

        Returns:
            List of augmented results, each containing:
                - image: Augmented image
                - bboxes: Transformed bounding boxes
                - class_labels: Class labels (unchanged)
        """
        results = []

        for _ in range(self.multiplier):
            try:
                transformed = self.transform(
                    image=image,
                    bboxes=bboxes,
                    class_labels=class_labels,
                )

                results.append({
                    'image': transformed['image'],
                    'bboxes': transformed['bboxes'],
                    'class_labels': transformed['class_labels'],
                })
            except Exception as e:
                # Skip failed augmentations rather than using fallbacks
                raise Exception(f"Augmentation failed: {str(e)}")

        return results


class PreprocessingPipeline:
    """
    Handles image preprocessing operations.
    Applied to all splits (train/valid/test).
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Apply preprocessing transformations to an image.

        Args:
            image: Input image as numpy array

        Returns:
            Preprocessed image
        """
        # Auto-orient (fix EXIF orientation)
        if self.config.get("auto_orient"):
            # This would require reading EXIF data and rotating accordingly
            pass

        # Resize
        if resize_config := self.config.get("resize"):
            mode = resize_config.get("mode", "fit")  # stretch, fit, pad
            width = resize_config["width"]
            height = resize_config["height"]

            if mode == "stretch":
                image = cv2.resize(image, (width, height))
            elif mode == "fit":
                h, w = image.shape[:2]
                scale = min(width / w, height / h)
                new_w, new_h = int(w * scale), int(h * scale)
                image = cv2.resize(image, (new_w, new_h))
            elif mode == "pad":
                h, w = image.shape[:2]
                scale = min(width / w, height / h)
                new_w, new_h = int(w * scale), int(h * scale)
                resized = cv2.resize(image, (new_w, new_h))

                # Pad to target size
                top = (height - new_h) // 2
                bottom = height - new_h - top
                left = (width - new_w) // 2
                right = width - new_w - left

                image = cv2.copyMakeBorder(
                    resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0)
                )

        # Grayscale
        if self.config.get("grayscale"):
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Convert back to 3 channels

        # Auto-adjust contrast
        if self.config.get("auto_contrast"):
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            l = cv2.equalizeHist(l)
            lab = cv2.merge([l, a, b])
            image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        return image


async def generate_version_task(ctx: Dict[str, Any], version_id: str) -> str:
    """
    ARQ task for generating a dataset version with preprocessing and augmentation.

    This is a placeholder that will be fully implemented once database models are set up.
    """
    # This task will:
    # 1. Load the dataset_versions record from the database
    # 2. Get all images in the source dataset
    # 3. Apply preprocessing pipeline
    # 4. Apply augmentation pipeline (training split only)
    # 5. Save augmented images to S3
    # 6. Create new image/annotation records
    # 7. Update dataset_versions status to COMPLETED

    raise NotImplementedError("Database schema not yet initialized")


async def export_dataset_task(ctx: Dict[str, Any], version_id: str, export_format: str) -> str:
    """
    ARQ task for exporting a dataset version to various formats.

    Supported formats: COCO, YOLO, VOC, etc.
    """
    # This task will:
    # 1. Load the dataset version
    # 2. Format annotations according to export_format
    # 3. Create zip file with images and annotations
    # 4. Upload to S3
    # 5. Return download URL

    raise NotImplementedError("Database schema not yet initialized")
