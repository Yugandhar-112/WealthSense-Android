"""
Trains a small merchant-category classifier and exports it as model.tflite.

Run this locally (NOT in the Android project) after: pip install tensorflow

    cd ml_training
    python train_model.py

Output: model.tflite in this same folder. Copy it into:
    app/src/main/assets/model.tflite

Model design (kept deliberately simple - this is a tiny on-device classifier,
not a production NLP model):
  - Input: a 49-length "bag of words" float vector. Position i is 1.0 if
    vocabulary word i appears anywhere in the merchant text, else 0.0.
    (See build_vocab.py for how the 49 words were chosen from dataset.py.)
  - Two small Dense layers, softmax output over 8 categories.

This must produce EXACTLY the same input encoding that CategoryClassifier.kt
builds at inference time, or predictions will be meaningless. If you ever
change dataset.py, re-run build_vocab.py, update the `vocab` map in
CategoryClassifier.kt to match, then re-run this script.
"""
import json
import numpy as np
import tensorflow as tf

from dataset import DATA, CATEGORIES
from build_vocab import tokenize

with open("vocab.json") as f:
    VOCAB = json.load(f)

VOCAB_SIZE = len(VOCAB)
NUM_CATEGORIES = len(CATEGORIES)
CATEGORY_TO_IDX = {c: i for i, c in enumerate(CATEGORIES)}


def encode(text: str) -> np.ndarray:
    vec = np.zeros(VOCAB_SIZE, dtype=np.float32)
    for tok in tokenize(text):
        if tok in VOCAB:
            vec[VOCAB[tok]] = 1.0
    return vec


def build_dataset():
    X = np.stack([encode(text) for text, _ in DATA])
    y = np.array([CATEGORY_TO_IDX[cat] for _, cat in DATA], dtype=np.int32)
    return X, y


def build_model() -> tf.keras.Model:
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(VOCAB_SIZE,)),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),
    ])
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main():
    X, y = build_dataset()
    print(f"Dataset: {X.shape[0]} examples, {VOCAB_SIZE} vocab features, {NUM_CATEGORIES} categories")

    # Small dataset -> simple shuffle split rather than stratified k-fold
    rng = np.random.default_rng(42)
    idx = rng.permutation(len(X))
    split = int(0.85 * len(X))
    train_idx, val_idx = idx[:split], idx[split:]

    model = build_model()
    model.fit(
        X[train_idx], y[train_idx],
        validation_data=(X[val_idx], y[val_idx]),
        epochs=60,
        batch_size=8,
        verbose=2,
    )

    loss, acc = model.evaluate(X[val_idx], y[val_idx], verbose=0)
    print(f"\nValidation accuracy: {acc:.2%}")

    # --- Convert to TFLite ---
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    with open("model.tflite", "wb") as f:
        f.write(tflite_model)

    print(f"\nSaved model.tflite ({len(tflite_model)} bytes)")
    print("Copy this file to: app/src/main/assets/model.tflite")

    # Quick sanity check with the actual TFLite interpreter (not just Keras)
    interpreter = tf.lite.Interpreter(model_content=tflite_model)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    test_merchants = ["SWIGGY BANGALORE", "AMAZON PAY", "UBER INDIA SYSTEMS", "NETFLIX COM", "APOLLO PHARMACY"]
    print("\nSanity check predictions:")
    for merchant in test_merchants:
        vec = encode(merchant).reshape(1, -1)
        interpreter.set_tensor(input_details[0]["index"], vec)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]["index"])[0]
        predicted = CATEGORIES[int(np.argmax(output))]
        confidence = float(np.max(output))
        print(f"  {merchant:25s} -> {predicted:15s} ({confidence:.0%} confidence)")


if __name__ == "__main__":
    main()
