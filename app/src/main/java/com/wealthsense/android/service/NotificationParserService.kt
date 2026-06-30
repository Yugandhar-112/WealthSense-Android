package com.wealthsense.android.service

import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import com.wealthsense.android.data.AppDatabase
import com.wealthsense.android.data.Transaction
import com.wealthsense.android.ml.CategoryClassifier
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.util.regex.Pattern

class NotificationParserService : NotificationListenerService() {

    private lateinit var database: AppDatabase
    private lateinit var classifier: CategoryClassifier
    private val serviceScope = CoroutineScope(Dispatchers.IO)

    private val filterPackages = hashSetOf(
        "com.google.android.apps.nbu.paisa.user", // Google Pay
        "com.phonepe.app",                        // PhonePe
        "net.one97.paytm",                        // Paytm
        "com.google.android.apps.messaging"       // SMS App Alert Fallback
    )

    override fun onCreate() {
        super.onCreate()
        database = AppDatabase.getDatabase(this)
        classifier = CategoryClassifier(this)
    }

    override fun onNotificationPosted(sbn: StatusBarNotification) {
        if (!filterPackages.contains(sbn.packageName)) return

        val extras = sbn.notification.extras
        val title = extras.getString("android.title") ?: ""
        val text = extras.getCharSequence("android.text")?.toString() ?: ""
        val content = "$title $text".lowercase()

        // Debited Assertion Filter
        if (content.contains("debited") || content.contains("spent") || content.contains("sent")) {
            parsePayload(content)
        }
    }

    private fun parsePayload(rawText: String) {
        val amountRegex = "(?:rs\\.?|inr|₹)\\s*([0-9,]+\\.?[0-9]*)"
        val merchantRegex = "(?:to|at)\\s+([a-z0-9\\s\\.]+?)(?:via|on|ref|$)"

        val amountPattern = Pattern.compile(amountRegex, Pattern.CASE_INSENSITIVE)
        val merchantPattern = Pattern.compile(merchantRegex, Pattern.CASE_INSENSITIVE)

        val amountMatcher = amountPattern.matcher(rawText)
        val merchantMatcher = merchantPattern.matcher(rawText)

        val amount = if (amountMatcher.find()) amountMatcher.group(1)?.replace(",", "")?.toDoubleOrNull() else null
        val merchant = if (merchantMatcher.find()) merchantMatcher.group(1)?.trim()?.uppercase() else "UNKNOWN MERCHANT"

        if (amount != null) {
            serviceScope.launch {
                val predictedCategory = classifier.classifyMerchant(merchant ?: "")
                val tx = Transaction(amount = amount, merchant = merchant ?: "UNKNOWN", category = predictedCategory)
                database.transactionDao().insertTransaction(tx)
            }
        }
    }
}