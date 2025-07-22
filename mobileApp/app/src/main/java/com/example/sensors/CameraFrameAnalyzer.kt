package com.example.sensors

import android.graphics.Bitmap
import android.graphics.ImageFormat
import android.media.Image
import android.util.Base64
import android.util.Log
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer

class CameraFrameAnalyzer(private val socketClient: WebSocketClient) : ImageAnalysis.Analyzer {

    override fun analyze(imageProxy: ImageProxy) {
        val image = imageProxy.image ?: return
        val bitmap = image.toBitmap() ?: return

        val outputStream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.JPEG, 50, outputStream)
        val base64Image = Base64.encodeToString(outputStream.toByteArray(), Base64.NO_WRAP)

        socketClient.send(base64Image)
        imageProxy.close()
    }

    private fun Image.toBitmap(): Bitmap? {
        if (format != ImageFormat.YUV_420_888) return null
        val yBuffer: ByteBuffer = planes[0].buffer
        val uBuffer: ByteBuffer = planes[1].buffer
        val vBuffer: ByteBuffer = planes[2].buffer
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
