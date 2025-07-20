package com.example.sensors

import android.content.Context
import android.content.pm.PackageManager
import android.hardware.*
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.sensors.ui.theme.SensorsTheme
import androidx.camera.core.CameraSelector
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.viewinterop.AndroidView
import androidx.activity.compose.BackHandler
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : ComponentActivity(), SensorEventListener {

    private lateinit var sensorManager: SensorManager
    private lateinit var sensorList: List<Sensor>
    private val sensorDataMap = mutableStateMapOf<String, List<Float>>()

    private var isStreaming = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // ✅ Request Camera Permission at runtime
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(android.Manifest.permission.CAMERA),
                100
            )
        }

        sensorManager = getSystemService(Context.SENSOR_SERVICE) as SensorManager
        sensorList = sensorManager.getSensorList(Sensor.TYPE_ALL)

        enableEdgeToEdge()

        setContent {
            SensorsTheme {
                var showCamera by remember { mutableStateOf(false) }
                var streamingStarted by remember { mutableStateOf(false) }

                Scaffold(modifier = Modifier.fillMaxSize()) { padding ->
                    if (showCamera) {
                        CameraScreen(onBack = { showCamera = false })
                    } else {
                        SensorDataScreen(
                            sensorData = sensorDataMap,
                            onStartStreaming = {
                                if (!isStreaming) {
                                    isStreaming = true
                                    streamingStarted = true
                                    for (sensor in sensorList) {
                                        sensorManager.registerListener(
                                            this@MainActivity,
                                            sensor,
                                            SensorManager.SENSOR_DELAY_NORMAL
                                        )
                                    }
                                }
                                showCamera = true
                            },
                            isStreaming = streamingStarted,
                            modifier = Modifier.padding(padding)
                        )
                    }
                }
            }
        }
    }

    override fun onSensorChanged(event: SensorEvent?) {
        if (!isStreaming || event == null) return
        sensorDataMap[event.sensor.name] = event.values.toList()
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}

    override fun onDestroy() {
        super.onDestroy()
        sensorManager.unregisterListener(this)
    }
}

@Composable
fun SensorDataScreen(
    sensorData: Map<String, List<Float>>,
    onStartStreaming: () -> Unit,
    isStreaming: Boolean,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.padding(16.dp)) {
        Button(
            onClick = { onStartStreaming() },
            enabled = !isStreaming,
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp)
        ) {
            Text(text = if (isStreaming) "Streaming Started" else "Start Camera + Sensor Streaming")
        }

        LazyColumn {
            items(sensorData.entries.toList()) { (sensorName, values) ->
                Column(modifier = Modifier.padding(vertical = 8.dp)) {
                    Text(text = sensorName, style = MaterialTheme.typography.titleMedium)
                    Text(text = "Values: ${values.joinToString(", ")}")
                }
            }
        }
    }
}

@Composable
fun CameraScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current

    AndroidView(
        factory = {
            PreviewView(context).apply {
                val cameraProviderFuture = ProcessCameraProvider.getInstance(context)
                cameraProviderFuture.addListener({
                    val cameraProvider = cameraProviderFuture.get()
                    val preview = Preview.Builder().build()
                    val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

                    preview.setSurfaceProvider(this.surfaceProvider)

                    try {
                        cameraProvider.unbindAll()
                        cameraProvider.bindToLifecycle(
                            lifecycleOwner,
                            cameraSelector,
                            preview
                        )
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                }, ContextCompat.getMainExecutor(context))
            }
        },
        modifier = Modifier.fillMaxSize()
    )

    BackHandler(onBack = onBack)
}
