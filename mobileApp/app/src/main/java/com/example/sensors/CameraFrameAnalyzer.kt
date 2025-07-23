package com.example.sensors

import android.graphics.Bitmap
import android.graphics.ImageFormat
import android.media.Image
import android.util.Log
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer

class CameraFrameAnalyzer(private val socketClient: WebSocketClient) : ImageAnalysis.Analyzer {

    override fun analyze(imageProxy: ImageProxy) {
        val image = imageProxy.image ?: run {
            imageProxy.close()
            return
        }

        val originalBitmap = image.toBitmap() ?: run {
            imageProxy.close()
            return
        }

        // ✅ Resize to 640x480 before sending
        val resizedBitmap = Bitmap.createScaledBitmap(originalBitmap, 640, 480, true)

        val outputStream = ByteArrayOutputStream()
        resizedBitmap.compress(Bitmap.CompressFormat.JPEG, 60, outputStream)
        val jpegBytes = outputStream.toByteArray()

        // Send resized JPEG bytes
        socketClient.sendBytes(jpegBytes)

        imageProxy.close()
    }


    private fun Image.toBitmap(): Bitmap? {
        if (format != ImageFormat.YUV_420_888) return null

        val yBuffer = planes[0].buffer
        val uBuffer = planes[1].buffer
        val vBuffer = planes[2].buffer

        val ySize = yBuffer.remaining()
        val uSize = uBuffer.remaining()
        val vSize = vBuffer.remaining()

        val nv21 = ByteArray(ySize + uSize + vSize)

        yBuffer.get(nv21, 0, ySize)
        vBuffer.get(nv21, ySize, vSize)
        uBuffer.get(nv21, ySize + vSize, uSize)

        return YuvUtils.nv21ToBitmap(nv21, width, height)
    }
}
