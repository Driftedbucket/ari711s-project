import os
import sys
import argparse
import random

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = (30,30)

def load_data(dataset_path, max_per_class=None, sample_fraction=None):
def build_model(input_shape, num_classes):
def plot_samples(X, y_true, y_pred, class_map=None, n=8):
def main():










