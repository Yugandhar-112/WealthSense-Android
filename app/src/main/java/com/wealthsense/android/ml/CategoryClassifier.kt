package com.wealthsense.android.ml

import android.content.Context
import org.tensorflow.lite.Interpreter
import java.io.FileInputStream
import java.nio.MappedByteBuffer
import java.nio.channels.FileChannel

class CategoryClassifier(context: Context) {
    private var interpreter: Interpreter? = null
    // Static vocabulary mapping fallback from WealthSense core structure
    private val vocab = mapOf("swiggy" to 1, "zomato" to 2, "amazon" to 3, "uber" to 4, "blinkit" to 5)
    private val categories = listOf("Food", "Shopping", "Transport", "Groceries", "Miscellaneous")

    init {
        try {
            val fileBuffer = loadModelFile(context, "model.tflite")
            // Prevent crashes during testing if the local asset file is empty (0 bytes)
            if (fileBuffer.capacity() > 0) {
                interpreter = Interpreter(fileBuffer)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun loadModelFile(context: Context, modelName: String): MappedByteBuffer {
        val fileDescriptor = context.assets.openFd(modelName)
        val inputStream = FileInputStream(fileDescriptor.fileDescriptor)
        val fileChannel = inputStream.channel
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, fileDescriptor.startOffset, fileDescriptor.declaredLength)
    }

    fun classifyMerchant(merchantName: String): String {
        // Fallback gracefully if the interpreter wasn't initialized due to an empty model asset
        if (interpreter == null) {
            return fallbackHeuristicClassifier(merchantName)
        }
        
        try {
            val tokens = merchantName.lowercase().split(" ")
            val inputVector = FloatArray(10) { 0.0f }
            
            for (i in tokens.indices) {
                if (i >= 10) break
                inputVector[i] = vocab[tokens[i]]?.toFloat() ?: 0.0f
            }

            val outputArray = Array(1) { FloatArray(categories.size) }
            interpreter?.run(arrayOf(inputVector), outputArray)

            val maxIndex = outputArray[0].indices.maxByOrNull { outputArray[0][it] } ?: 0
            return categories[maxIndex]
        } catch (e: Exception) {
            e.printStackTrace()
            return fallbackHeuristicClassifier(merchantName)
        }
    }

    // High-performance fallback string matcher until the binary ML asset weights are compiled
    private fun fallbackHeuristicClassifier(merchantName: String): String {
        val name = merchantName.lowercase()
        return when {
            name.contains("swiggy") || name.contains("zomato") || name.contains("eats") -> "Food"
            name.contains("amazon") || name.contains("flipkart") || name.contains("myntra") -> "Shopping"
            name.contains("uber") || name.contains("ola") || name.contains("rapido") -> "Transport"
            name.contains("blinkit") || name.contains("zepto") || name.contains("instamart") -> "Groceries"
            else -> "Miscellaneous"
        }
    }
}