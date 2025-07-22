package com.example.sensors

import android.util.Log
import okhttp3.*
import okio.ByteString
import java.util.concurrent.TimeUnit

class WebSocketClient {

    private lateinit var webSocket: WebSocket
    private val client = OkHttpClient.Builder()
        .readTimeout(0, TimeUnit.MILLISECONDS)
        .build()

    fun connect(serverUrl: String) {
        val request = Request.Builder().url(serverUrl).build()
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(ws: WebSocket, response: Response) {
                Log.d("WebSocket", "Connected ✅")
            }

            override fun onMessage(ws: WebSocket, text: String) {
                Log.d("WebSocket", "Received message: $text")
            }

            override fun onFailure(ws: WebSocket, t: Throwable, response: Response?) {
                Log.e("WebSocket", "Error: ${t.localizedMessage}")
            }

            override fun onClosed(ws: WebSocket, code: Int, reason: String) {
                Log.d("WebSocket", "Closed: $reason")
            }
        })
    }

    fun send(base64Image: String) {
        if (::webSocket.isInitialized) {
            webSocket.send("{\"type\": \"frame\", \"data\": \"$base64Image\"}")
        }
    }
}
