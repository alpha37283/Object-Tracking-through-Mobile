package com.example.sensors

import android.graphics.Bitmap
import android.graphics.ImageFormat
import android.graphics.YuvImage
import java.io.ByteArrayOutputStream

object YuvUtils {
    fun nv21ToBitmap(nv21: ByteArray, width: Int, height: Int): Bitmap? {
        val yuvImage = YuvImage(nv21, ImageFormat.NV21, width, height, null)
        val out = ByteArrayOutputStream()
        yuvImage.compressToJpeg(android.graphics.Rect(0, 0, width, height), 90, out)
        val imageBytes = out.toByteArray()
        return android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
    }
}


