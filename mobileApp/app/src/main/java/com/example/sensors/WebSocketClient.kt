package com.example.sensors

import android.util.Log
import okhttp3.*
import java.util.concurrent.TimeUnit
import okio.ByteString


class WebSocketClient {

    private var webSocket: WebSocket? = null
    private var overlay: DetectionOverlay? = null

    fun attachOverlay(view: DetectionOverlay) {
        overlay = view
    }

    private val client = OkHttpClient.Builder()
        .readTimeout(0, TimeUnit.MILLISECONDS)
        .build()

    fun connect(serverUrl: String) {
        val request = Request.Builder().url(serverUrl).build()
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(ws: WebSocket, response: Response) {
                Log.d("WebSocket", "✅ Connected to $serverUrl")
            }

            override fun onMessage(ws: WebSocket, text: String) {
                Log.d("WebSocket", "📩 Received: $text")
                overlay?.post {
                    overlay?.updateDetections(text)
                }
            }

            override fun onFailure(ws: WebSocket, t: Throwable, response: Response?) {
                Log.e("WebSocket", "❌ WebSocket Error: ${t.localizedMessage}", t)
            }

            override fun onClosed(ws: WebSocket, code: Int, reason: String) {
                Log.d("WebSocket", "🔌 Disconnected: $reason")
            }
        })
    }

    fun sendBytes(data: ByteArray) {
        webSocket?.let {
            it.send(ByteString.of(*data))
            Log.d("WebSocket", "📤 Sent ${data.size} bytes")
        } ?: Log.w("WebSocket", "⚠️ Tried to send but socket is null")
    }
}
