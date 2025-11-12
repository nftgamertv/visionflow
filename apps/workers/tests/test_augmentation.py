"""
Augmentation pipeline tests
"""
import numpy as np
from app.tasks.augmentation import AugmentationPipeline, PreprocessingPipeline


def test_augmentation_pipeline_init():
    """Test augmentation pipeline initialization"""
    config = {
        "flip_horizontal": True,
        "multiplier": 2
    }
    pipeline = AugmentationPipeline(config)
    assert pipeline.multiplier == 2


def test_preprocessing_pipeline_init():
    """Test preprocessing pipeline initialization"""
    config = {
        "grayscale": True
    }
    pipeline = PreprocessingPipeline(config)
    assert pipeline.config == config
