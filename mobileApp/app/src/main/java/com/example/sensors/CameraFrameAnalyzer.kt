package com.example.sensors

import android.graphics.Bitmap
import android.graphics.ImageFormat
import android.media.Image
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import java.io.ByteArrayOutputStream

class CameraFrameAnalyzer(private val socketClient: WebSocketClient) : ImageAnalysis.Analyzer {

    override fun analyze(imageProxy: ImageProxy) {
        val image = imageProxy.image ?: run {
            imageProxy.close()
            return
        }

        val nv21Bytes = YuvUtils.YUV_420_888toNv21(image)
        val bitmap = YuvUtils.nv21ToBitmap(nv21Bytes, image.width, image.height) ?: run {
            imageProxy.close()
            return
        }

        // Resize to 640x480 before sending
        val resizedBitmap = Bitmap.createScaledBitmap(bitmap, 640, 480, true)

        val outputStream = ByteArrayOutputStream()
        resizedBitmap.compress(Bitmap.CompressFormat.JPEG, 60, outputStream)
        val jpegBytes = outputStream.toByteArray()

        // Send JPEG over WebSocket
        socketClient.sendBytes(jpegBytes)

        imageProxy.close()
    }
}
