// DetectionOverlay.kt
package com.example.sensors

import android.content.Context
import android.graphics.*
import android.util.AttributeSet
import android.view.View
import org.json.JSONArray
import org.json.JSONObject

class DetectionOverlay(context: Context, attrs: AttributeSet?) : View(context, attrs) {

    private val boxPaint = Paint().apply {
        color = Color.RED
        strokeWidth = 4f
        style = Paint.Style.STROKE
    }

    private val textPaint = Paint().apply {
        color = Color.WHITE
        textSize = 40f
        style = Paint.Style.FILL
    }

    private var boxes: List<DetectionBox> = emptyList()

    fun updateDetections(jsonString: String) {
        val newBoxes = mutableListOf<DetectionBox>()
        try {
            val json = JSONObject(jsonString)
            val detections: JSONArray = json.getJSONArray("detections")

            // Input frame size from Android → Python → back to Android
            val inputWidth = 640f
            val inputHeight = 480f

            // Output view size (this overlay's actual size)
            val scaleX = width / inputWidth
            val scaleY = height / inputHeight

            for (i in 0 until detections.length()) {
                val obj = detections.getJSONObject(i)
                val bbox = obj.getJSONArray("bbox")

                // Scale each coordinate
                val left = (bbox.getInt(0) * scaleX).toInt()
                val top = (bbox.getInt(1) * scaleY).toInt()
                val right = (bbox.getInt(2) * scaleX).toInt()
                val bottom = (bbox.getInt(3) * scaleY).toInt()

                newBoxes.add(
                    DetectionBox(
                        left = left,
                        top = top,
                        right = right,
                        bottom = bottom,
                        label = "${obj.getString("class")} ${(obj.getDouble("confidence") * 100).toInt()}%"
                    )
                )
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }

        boxes = newBoxes
        invalidate()
    }


    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        for (box in boxes) {
            canvas.drawRect(box.left.toFloat(), box.top.toFloat(), box.right.toFloat(), box.bottom.toFloat(), boxPaint)
            canvas.drawText(box.label, box.left.toFloat(), box.top.toFloat() - 10, textPaint)
        }
    }

    data class DetectionBox(
        val left: Int,
        val top: Int,
        val right: Int,
        val bottom: Int,
        val label: String
    )
}
