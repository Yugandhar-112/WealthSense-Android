package com.wealthsense.android.ml

import android.content.Context
import org.tensorflow.lite.Interpreter
import java.io.FileInputStream
import java.nio.MappedByteBuffer
import java.nio.channels.FileChannel

class CategoryClassifier(context: Context) {
    private var interpreter: Interpreter? = null
    // Static vocabulary map mimicking target features from WealthSense-ML
    private val vocab = mapOf("swiggy" to 1, "zomato" to 2, "amazon" to 3, "uber" to 4, "blinkit" to 5)
    private val categories = listOf("Food", "Shopping", "Transport", "Groceries", "Miscellaneous")

    init {
        try {
            interpreter = Interpreter(loadModelFile(context, "model.tflite"))
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
        if (interpreter == null) return "Miscellaneous"
        
        val tokens = merchantName.lowercase().split(" ")
        val inputVector = FloatArray(10) { 0.0f } // Static input buffer size matching ML baseline
        
        for (i in tokens.indices) {
            if (i >= 10) break
            inputVector[i] = vocab[tokens[i]]?.toFloat() ?: 0.0f
        }

        val outputArray = Array(1) { FloatArray(categories.size) }
        interpreter?.run(arrayOf(inputVector), outputArray)

        val maxIndex = outputArray[0].indices.maxByOrNull { outputArray[0][it] } ?: 0
        return categories[maxIndex]
    }
}