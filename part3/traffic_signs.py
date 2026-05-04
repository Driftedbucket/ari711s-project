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
    images = []
    labels = []
    classes = []
    # Expect subfolders named 0..42 (or any integer labels)
    for entry in sorted(os.listdir(dataset_path)):
        full = os.path.join(dataset_path, entry)
        if not os.path.isdir(full):
            continue
        try:
            label = int(entry)
        except ValueError:
            # skip unexpected folders
            continue
        classes.append(label)
        # Collect files for this class and optionally sample a subset
        files = [f for f in os.listdir(full) if f.lower().endswith(('.ppm', '.jpg', '.jpeg', '.png'))]
        if len(files) == 0:
            continue
        # Determine sample size
        if max_per_class is not None:
            k = min(max_per_class, len(files))
            chosen = random.sample(files, k)
        elif sample_fraction is not None and 0.0 < sample_fraction < 1.0:
            k = max(1, int(len(files) * sample_fraction))
            chosen = random.sample(files, k)
        else:
            chosen = files
  
        for fname in chosen:
            fpath = os.path.join(full, fname)
            img = cv2.imread(fpath)
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, IMG_SIZE)
            images.append(img)
            labels.append(label)
    if len(images) == 0:
        raise RuntimeError(f'No images found in {dataset_path}')

    X = np.array(images, dtype='float32') / 255.0
    y = np.array(labels, dtype='int32')
    # Use unique labels to determine number of classes (robust if labels aren't contiguous)
    num_classes = int(np.unique(y).shape[0])
    y_cat = to_categorical(y, num_classes)
    return X, y_cat, y, num_classes


def build_model(input_shape, num_classes):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        BatchNormalization(),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(),
        Dropout(0.25),

        Conv2D(64, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(),
        Dropout(0.25),

        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def plot_samples(X, y_true, y_pred, class_map=None, n=8):
    idx = list(range(len(X)))
    random.shuffle(idx)
    idx = idx[:n]
    plt.figure(figsize=(12, 3))
    for i, k in enumerate(idx):
        plt.subplot(1, n, i+1)
        plt.axis('off')
        plt.imshow(X[k])
        true = y_true[k]
        pred = y_pred[k]
        tlabel = class_map[true] if class_map else str(true)
        plabel = class_map[pred] if class_map else str(pred)
        color = 'green' if true == pred else 'red'
        plt.title(f'T:{tlabel}\nP:{plabel}', color=color, fontsize=8)
    plt.tight_layout()
    plt.show()
def main():

    parser = argparse.ArgumentParser(description='Train a traffic sign classifier (GTSRB)')
    parser.add_argument('dataset', help='Path to dataset folder (contains numeric subfolders)')
    parser.add_argument('model_out', nargs='?', default=None, help='Optional output model filename (e.g., model.h5)')
    parser.add_argument('--epochs', type=int, default=15)
    parser.add_argument('--batch', type=int, default=64)
    parser.add_argument('--max-per-class', type=int, default=None,
                        help='Limit number of images per class (e.g., 100)')
    parser.add_argument('--sample-fraction', type=float, default=None,
                        help='Sample fraction of images per class (0.0-1.0)')
    parser.add_argument('--no-plot', action='store_true', help='Do not show sample plots')
    args = parser.parse_args()

    dataset_path = args.dataset
    model_out = args.model_out
    no_plot = getattr(args, 'no_plot', False)

    if not os.path.isdir(dataset_path):
        print(f"Dataset path not found or not a directory: {dataset_path}")
        sys.exit(1)

    print('Loading data...')
    X, y_cat, y_raw, num_classes = load_data(dataset_path, max_per_class=args.max_per_class, sample_fraction=args.sample_fraction)
    print(f'Data loaded: {X.shape[0]} images, {num_classes} classes')

    X_train, X_test, y_train, y_test, y_train_raw, y_test_raw = train_test_split(
        X, y_cat, y_raw, test_size=0.2, random_state=42, stratify=y_raw)

    print('Building model...')
    model = build_model(input_shape=X.shape[1:], num_classes=num_classes)
    model.summary()

    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=False,
        fill_mode='nearest'
    )

    steps_per_epoch = max(1, len(X_train) // args.batch)
    print('Training model...')
    history = model.fit(
        datagen.flow(X_train, y_train, batch_size=args.batch),
        steps_per_epoch=steps_per_epoch,
        epochs=args.epochs,
        validation_data=(X_test, y_test),
        verbose=2
    )









