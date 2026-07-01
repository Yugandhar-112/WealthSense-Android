package com.wealthsense.android

import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.recyclerview.widget.LinearLayoutManager
import com.wealthsense.android.data.AppDatabase
import com.wealthsense.android.databinding.ActivityMainBinding
import com.wealthsense.android.ui.TransactionAdapter
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private lateinit var adapter: TransactionAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        adapter = TransactionAdapter()
        binding.rvTransactions.layoutManager = LinearLayoutManager(this)
        binding.rvTransactions.adapter = adapter

        binding.btnPermission.setOnClickListener {
            // Forward user directly to Notification Listener Settings configuration area
            startActivity(Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS))
        }

        observeTransactions()
    }

    private fun observeTransactions() {
        val database = AppDatabase.getDatabase(this)

        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                database.transactionDao().getAllTransactions().collect { transactions ->
                    adapter.submitList(transactions)
                    val hasData = transactions.isNotEmpty()
                    binding.rvTransactions.visibility = if (hasData) View.VISIBLE else View.GONE
                    binding.tvEmptyState.visibility = if (hasData) View.GONE else View.VISIBLE
                }
            }
        }
    }
}
