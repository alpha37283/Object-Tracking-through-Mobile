package com.example.sensors

import android.graphics.Bitmap
import android.graphics.ImageFormat
import android.graphics.YuvImage
import android.media.Image
import java.io.ByteArrayOutputStream

object YuvUtils {

    fun YUV_420_888toNv21(image: Image): ByteArray {
        val width = image.width
        val height = image.height

        val ySize = width * height
        val uvSize = width * height / 4

        val nv21 = ByteArray(ySize + uvSize * 2)

        val yBuffer = image.planes[0].buffer
        val uBuffer = image.planes[1].buffer
        val vBuffer = image.planes[2].buffer

        val rowStride = image.planes[0].rowStride
        val pixelStride = image.planes[1].pixelStride

        var pos = 0

        for (row in 0 until height) {
            yBuffer.position(row * rowStride)
            yBuffer.get(nv21, pos, width)
            pos += width
        }

        val chromaRowStride = image.planes[1].rowStride
        val chromaPixelStride = image.planes[1].pixelStride

        val uvHeight = height / 2
        val uvWidth = width / 2

        for (row in 0 until uvHeight) {
            for (col in 0 until uvWidth) {
                val uIndex = row * chromaRowStride + col * chromaPixelStride
                val vIndex = row * image.planes[2].rowStride + col * image.planes[2].pixelStride
                nv21[pos++] = vBuffer.get(vIndex)
                nv21[pos++] = uBuffer.get(uIndex)
            }
        }

        return nv21
    }

    fun nv21ToBitmap(nv21: ByteArray, width: Int, height: Int): Bitmap? {
        val yuvImage = YuvImage(nv21, ImageFormat.NV21, width, height, null)
        val out = ByteArrayOutputStream()
        yuvImage.compressToJpeg(android.graphics.Rect(0, 0, width, height), 90, out)
        val imageBytes = out.toByteArray()
        return android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
    }
}
