# WealthSense-Android

Android client for automated expense tracking. Parses transactional notifications and applies a locally-run hybrid classifier (trained TFLite model + keyword fallback) for real-time categorization — no data ever leaves the device.

## Directory Structural Layout

```text
WealthSense-Android/
├── requirements.txt              # Python deps for training/converting the model (run on your PC, not on-device)
├── README.md
├── ml_training/                  # Model training pipeline (source of truth for the TFLite model)
│   ├── dataset.py                 # Labeled merchant-text -> category examples
│   ├── build_vocab.py             # Builds the bag-of-words vocabulary from dataset.py
│   ├── train_model.py             # Trains the classifier and exports model.tflite
│   └── vocab.json                 # Generated vocabulary (word -> input vector position)
└── app/
    ├── build.gradle.kts
    └── src/
        └── main/
            ├── AndroidManifest.xml
            ├── assets/
            │   └── model.tflite            # Trained classifier, loaded at runtime
            ├── java/
            │   └── com/
            │       └── wealthsense/
            │           └── android/
            │               ├── MainActivity.kt          # Transaction list UI + permission entry point
            │               ├── data/
            │               │   ├── AppDatabase.kt        # Room database setup
            │               │   ├── Transaction.kt        # Transaction entity
            │               │   └── TransactionDao.kt      # Queries (list all, insert)
            │               ├── ml/
            │               │   └── CategoryClassifier.kt  # Hybrid classifier (TFLite model + keyword fallback)
            │               ├── service/
            │               │   └── NotificationParserService.kt  # Listens to & parses payment notifications
            │               └── ui/
            │                   └── TransactionAdapter.kt  # RecyclerView adapter for the transaction list
            └── res/
                ├── drawable/
                │   └── ic_launcher_foreground.xml
                ├── layout/
                │   ├── activity_main.xml       # Main screen: title, transaction list, permission button
                │   └── item_transaction.xml    # Single row in the transaction list
                ├── mipmap-anydpi-v26/
                │   ├── ic_launcher.xml          # Adaptive app icon
                │   └── ic_launcher_round.xml
                └── values/
                    └── colors.xml
```

## Runtime Transaction Pipeline Flow

```
[System Notification Event]
│
▼ (Interception)
[NotificationParserService] ───► [Match Criteria Filter: debited / spent]
│
▼ (Regex Extraction)
[Amount & Merchant Entity Selection]
│
▼ (Hybrid Local Model Execution)
[CategoryClassifier: TFLite model (primary) → keyword fallback (if unsure/unavailable)]
│
▼ (Persistence Layer)
[Room Database Storage Execution]
│
▼ (UI)
[MainActivity + TransactionAdapter: live-updating transaction list]
```

## System Requirements & Permissions Architecture

| Permission Target | Enforcement Mode | Operational Scope |
|---|---|---|
| `BIND_NOTIFICATION_LISTENER_SERVICE` | Explicit User Authorization | Allows interception of system notifications |
| `POST_NOTIFICATIONS` | Runtime Handshake Alert | Dispatches diagnostic system UI transaction alerts |
| `RECEIVE_BOOT_COMPLETED` | System Intent | Restarts listening handlers automatically on device boot |

## Features & Implementation Mapping

* **Transaction List UI:** `MainActivity` + `TransactionAdapter` show all logged transactions (merchant, category, amount, timestamp) in a `RecyclerView`, live-updating via a Room `Flow`. An empty-state message shows before any transactions are recorded.
* **Hybrid On-Device Prediction Engine:** `CategoryClassifier` first tries the trained TFLite model (`model.tflite`). If the model isn't loaded (e.g. empty/missing asset) or isn't confident in its prediction (below a set threshold), it falls back to a hardcoded keyword matcher. This means the app degrades gracefully and never crashes or leaves a transaction uncategorized, even before a model is trained.
* **Regex Extraction Matrix:** Automatically strips structured entity variables away from transaction confirmation formats.
* **Storage Imprints:** Uses standard Android Room SQLite architecture protocols ensuring secure local operation without external network dependencies.

## Training / Updating the Classification Model

The TFLite model is *not* trained on-device — it's trained separately on your computer and the resulting `model.tflite` file is copied into the app.

```bash
pip install -r requirements.txt
cd ml_training
python train_model.py
```

This will:
1. Load labeled examples from `dataset.py`
2. Encode each merchant text as a bag-of-words vector using `vocab.json`
3. Train a small classifier (Dense → Dropout → Dense → softmax over 8 categories)
4. Convert it to TFLite and save `model.tflite` in `ml_training/`
5. Run a quick sanity check, printing sample predictions

Then copy the output into the app:
```bash
cp ml_training/model.tflite ../app/src/main/assets/model.tflite
```

**To improve accuracy:** add more real examples to `dataset.py` (the more realistic and varied, the better), then re-run `build_vocab.py` before `train_model.py` if you've introduced new vocabulary. If you change the vocabulary, update the `vocab` map in `CategoryClassifier.kt` to match exactly — the model and app must agree on what each input position means, or predictions will be meaningless.

**Categories:** `Food`, `Groceries`, `Shopping`, `Transport`, `Bills`, `Entertainment`, `Health`, `Miscellaneous`
