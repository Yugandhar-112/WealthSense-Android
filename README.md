# WealthSense-Android

Android client for automated expense tracking. Parses transactional notifications and applies local TensorFlow Lite models for real-time categorizations.

## Directory Structural Layout

```text
WealthSense-Android/
├── requirements.txt
├── README.md
└── app/
    ├── build.gradle.kts
    └── src/
        └── main/
            ├── AndroidManifest.xml
            ├── assets/
            │   └── model.tflite
            ├── java/
            │   └── com/
            │       └── wealthsense/
            │           └── android/
            │               ├── MainActivity.kt
            │               ├── data/
            │               │   ├── AppDatabase.kt
            │               │   ├── Transaction.kt
            │               │   └── TransactionDao.kt
            │               ├── ml/
            │               │   └── CategoryClassifier.kt
            │               └── service/
            │                   └── NotificationParserService.kt
            └── res/
                └── layout/
                    └── activity_main.xml
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
▼ (Local Model Execution)
[CategoryClassifier (TFLite Engine)]
│
▼ (Persistence Layer)
[Room Database Storage Execution]
```
## System Requirements & Permissions Architecture

| Permission Target | Enforcement Mode | Operational Scope |
|---|---|---|
| `BIND_NOTIFICATION_LISTENER_SERVICE` | Explicit User Authorization | Allows interception of system notifications |
| `POST_NOTIFICATIONS` | Runtime Handshake Alert | Dispatches diagnostic system UI transaction alerts |
| `RECEIVE_BOOT_COMPLETED` | System Intent | Restarts listening handlers automatically on device boot |

## Features & Implementation Mapping

* **On-Device Prediction Engine:** Transforms models down into an optimization footprint utilizing TFLite matrices (`model.tflite`).
* **Regex Extraction Matrix:** Automatically strips structured entity variables away from transaction confirmation formats.
* **Storage Imprints:** Uses standard Android Room SQLite architecture protocols ensuring secure local operation without external network dependencies.