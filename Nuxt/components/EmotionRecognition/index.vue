<template>
  <div>
    <ModeSelector 
      v-model="mode" 
      @update:mode="handleModeChange" 
    />
    
    <CameraView 
      :mode="mode"
      :is-recognizing="isRecognizing"
      :show-face-box="showFaceBox"
      :show-emotion-text="showEmotionText"
      :show-emoji="showEmoji"
      :media-stream="mediaStream"
      ref="cameraViewRef"
      @file-uploaded="handleFileUploaded"
    />
    
    <StatusBar :status="connectionStatus" />
    
    <ControlPanel 
      :mode="mode"
      :detector-models="detectorModels"
      :recognizer-models="recognizerModels"
      :selected-detector="selectedDetector"
      :selected-recognizer="selectedRecognizer"
      :is-recognizing="isRecognizing"
      :show-face-box="showFaceBox"
      :show-emotion-text="showEmotionText"
      :show-emoji="showEmoji"
      :is-mobile-device="isMobileDevice"
      :camera-facing="cameraFacing"
      :available-cameras="availableCameras"
      :selected-camera="selectedCamera"
      @update:selected-detector="selectedDetector = $event"
      @update:selected-recognizer="selectedRecognizer = $event"
      @update:selected-camera="handleCameraChange($event)"
      @toggle-recognition="toggleRecognition"
      @toggle-camera="toggleCamera"
      @update:show-face-box="showFaceBox = $event"
      @update:show-emotion-text="showEmotionText = $event"
      @update:show-emoji="showEmoji = $event"
    />
    
    <EmotionStats :emotion-stats="emotionStats" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import ModeSelector from './ModeSelector.vue'
import CameraView from './CameraView.vue'
import ControlPanel from './ControlPanel.vue'
import EmotionStats from './EmotionStats.vue'
import StatusBar from './StatusBar.vue'
import { useCamera } from '~/composables/useCamera'
import { useWebSocket } from '~/composables/useWebSocket'
import { useModels } from '~/composables/useModels'
import { useDeviceDetection } from '~/composables/useDeviceDetection'
import { emotionLabels } from '~/utils/emotions'
import { uploadImageForPrediction } from '~/services/api'

// 引用
const cameraViewRef = ref(null)

// 状态
const mode = ref('realtime') // 'realtime' 或 'upload'
const isRecognizing = ref(false)
const showFaceBox = ref(true)
const showEmotionText = ref(true)
const showEmoji = ref(true)
const connectionStatus = ref('')
const emotionStats = ref(Object.fromEntries(
  Object.keys(emotionLabels).map(key => [key, 0])
))
const uploadedFile = ref(null)
const isUploading = ref(false)

// 使用可组合函数
const { 
  isMobileDevice, checkMobileDevice 
} = useDeviceDetection()

const { 
  detectorModels, recognizerModels, 
  selectedDetector, selectedRecognizer, 
  fetchModels 
} = useModels(connectionStatus)

const { 
  mediaStream,availableCameras, selectedCamera, cameraFacing,
  setupCamera, releaseCamera, getAvailableCameras,
  handleCameraChange, toggleCamera
} = useCamera(connectionStatus, isMobileDevice)

const { 
  initWebSocket, closeWebSocket, 
  sendFrame, isFrameProcessing 
} = useWebSocket(
  selectedDetector, 
  selectedRecognizer, 
  connectionStatus, 
  handleRecognitionResult
)

// 处理文件上传
function handleFileUploaded(file) {
  uploadedFile.value = file
  
  // 如果正在识别，自动处理上传的图片
  if (isRecognizing.value && mode.value === 'upload') {
    processUploadedImage()
  }
}

// 处理模式变化
function handleModeChange(newMode) {
  console.log('模式已切换到:', newMode) // 添加日志
  mode.value = newMode // 确保模式被更新
  
  if (isRecognizing.value) {
    stopRecognition()
  }
  
  if (newMode === 'realtime') {
    cameraViewRef.value?.clearUploadedImage()
  } else {
    releaseCamera()
  }
}

// 切换识别状态
async function toggleRecognition() {
  if (isRecognizing.value) {
    stopRecognition()
  } else {
    startRecognition()
  }
}

// 开始识别
async function startRecognition() {
  try {
    if (!selectedDetector.value || !selectedRecognizer.value) {
      connectionStatus.value = '错误: 请先选择模型'
      return
    }
    
    if (mode.value === 'realtime') {
      connectionStatus.value = '正在设置摄像头...'
      await setupCamera()
      
      // 实时模式使用WebSocket
      await initWebSocket()
      isRecognizing.value = true
      startProcessing()
    } else {
      // 上传模式直接处理图片
      isRecognizing.value = true
      processUploadedImage()
    }
  } catch (error) {
    console.error('启动识别失败:', error)
    connectionStatus.value = `错误: 启动识别失败 - ${error.message}`
    isRecognizing.value = false
  }
}

// 停止识别
function stopRecognition() {
  isRecognizing.value = false
  
  if (mode.value === 'realtime') {
    closeWebSocket()
  }
  
  connectionStatus.value = '识别已停止'
  setTimeout(() => {
    if (connectionStatus.value === '识别已停止') {
      connectionStatus.value = ''
    }
  }, 2000)
}

// 开始处理视频帧
function startProcessing() {
  if (mode.value === 'realtime') {
    processVideoFrame()
  }
}

// 处理视频帧
function processVideoFrame() {
  if (!isRecognizing.value) return
  
  if (!isFrameProcessing.value) {
    const videoFrame = cameraViewRef.value?.captureVideoFrame()
    if (videoFrame) {
      sendFrame(videoFrame)
    }
  }
  
  // 无论是否处理帧，都继续请求下一帧动画
  requestAnimationFrame(processVideoFrame)
}

// 处理上传的图片
async function processUploadedImage() {
  if (!isRecognizing.value || isUploading.value) return
  
  const file = cameraViewRef.value?.getUploadedFile()
  
  if (!file) {
    connectionStatus.value = '请先上传图片'
    return
  }
  
  try {
    isUploading.value = true
    connectionStatus.value = '正在处理图片...'
    
    // 使用上传API进行识别
    const results = await uploadImageForPrediction(
      file, 
      selectedDetector.value, 
      selectedRecognizer.value
    )
    
    // 处理识别结果
    handleRecognitionResult(results)
    
    connectionStatus.value = '图片处理完成'
    setTimeout(() => {
      if (connectionStatus.value === '图片处理完成') {
        connectionStatus.value = ''
      }
    }, 2000)
  } catch (error) {
    console.error('图片处理失败:', error)
    connectionStatus.value = `错误: 图片处理失败 - ${error.message}`
  } finally {
    isUploading.value = false
  }
}

// 处理识别结果
function handleRecognitionResult(results) {
  if (!results || !results.length) return
  
  // 更新表情统计
  results.forEach(face => {
    const emotionCode = face[0]
    emotionStats.value[emotionCode]++
  })
  
  // 绘制结果
  cameraViewRef.value?.drawResults(results, showFaceBox.value, showEmotionText.value, showEmoji.value)
}

// 监听模型变化
watch([selectedDetector, selectedRecognizer], () => {
  if (isRecognizing.value) {
    // 如果是上传模式且模型变化，重新处理图片
    if (mode.value === 'upload') {
      processUploadedImage()
    } else {
      // 实时模式下，关闭连接然后重启识别
      closeWebSocket()
      nextTick(() => {
        startRecognition()
      })
    }
  }
})

// 监听mode变化
watch(mode, (newMode) => {
  // 如果切换到上传模式并且正在识别，且有上传的文件，则处理上传的图片
  if (newMode === 'upload' && isRecognizing.value && uploadedFile.value) {
    closeWebSocket() // 关闭可能存在的WebSocket连接
    processUploadedImage()
  }
})

// 组件加载和卸载
onMounted(async () => {
  checkMobileDevice()
  await fetchModels()
  await getAvailableCameras()
  
  // 检查摄像头API支持
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    connectionStatus.value = '警告: 此浏览器可能不支持摄像头访问。请使用最新版的Chrome或Safari。'
  }
  
  // 检查是否为HTTP连接（非localhost）
  if (window.location.protocol === 'http:' && window.location.hostname !== 'localhost') {
    connectionStatus.value = '警告: 在非HTTPS网站上通常无法访问摄像头。如果无法启动摄像头，请使用HTTPS连接。'
  }
})

onUnmounted(() => {
  releaseCamera()
  closeWebSocket()
})
</script>