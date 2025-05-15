<template>
  <div class="mb-8 relative">
    <div class="bg-gray-900 rounded-lg overflow-hidden aspect-video relative">
      <div 
        ref="videoContainer" 
        class="absolute inset-0 w-full h-full"
      >
        <video
          ref="videoEl"
          autoplay
          muted
          playsinline
          class="w-full h-full object-cover"
        ></video>
        <canvas
          ref="canvasEl"
          class="absolute inset-0 w-full h-full"
        ></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { drawFacesOnCanvas } from '~/utils/canvasUtils'

const props = defineProps({
  isRecognizing: {
    type: Boolean,
    default: false
  },
  showFaceBox: {
    type: Boolean,
    default: true
  },
  showEmotionText: {
    type: Boolean,
    default: true
  },
  showEmoji: {
    type: Boolean,
    default: true
  },
  mediaStream: {
    default: null
  }
})

// Refs
const videoEl = ref(null)
const videoContainer = ref(null)
const canvasEl = ref(null)

// 处理窗口大小变化
function handleResize() {
  if (!canvasEl.value || !videoContainer.value) return
  
  // 设置canvas尺寸与容器相同
  canvasEl.value.width = videoContainer.value.clientWidth
  canvasEl.value.height = videoContainer.value.clientHeight
}

// 捕获视频帧
function captureVideoFrame() {
  if (!videoEl.value || videoEl.value.readyState < 2) return null
  
  const canvas = document.createElement('canvas')
  const context = canvas.getContext('2d')
  canvas.width = videoEl.value.videoWidth
  canvas.height = videoEl.value.videoHeight
  context.drawImage(videoEl.value, 0, 0, canvas.width, canvas.height)
  
  return canvas
}

// 绘制结果
function drawResults(results) {
  if (!canvasEl.value || !results.length || !videoEl.value) return
  
  const ctx = canvasEl.value.getContext('2d')
  
  // 清除之前的绘制
  ctx.clearRect(0, 0, canvasEl.value.width, canvasEl.value.height)
  
  // 计算缩放比例
  const videoWidth = videoEl.value.videoWidth
  const videoHeight = videoEl.value.videoHeight
  const canvasWidth = canvasEl.value.width
  const canvasHeight = canvasEl.value.height
  
  // 计算缩放比例，保持宽高比
  const scaleX = canvasWidth / videoWidth
  const scaleY = canvasHeight / videoHeight
  const scale = Math.min(scaleX, scaleY)
  
  // 计算居中偏移
  const offsetX = (canvasWidth - videoWidth * scale) / 2
  const offsetY = (canvasHeight - videoHeight * scale) / 2
  
  // 保存当前上下文状态
  ctx.save()
  
  // 应用缩放和偏移
  ctx.translate(offsetX, offsetY)
  ctx.scale(scale, scale)
  
  // 绘制人脸框和表情
  drawFacesOnCanvas(ctx, results, props.showFaceBox, props.showEmotionText, props.showEmoji)
  
  // 恢复上下文状态
  ctx.restore()
}

// 监听媒体流变化
watch(() => props.mediaStream, (newStream) => {
  if (newStream && videoEl.value) {
    videoEl.value.srcObject = newStream
  }
})

onMounted(() => {
  // 监听窗口尺寸变化
  window.addEventListener('resize', handleResize)
  // 初始化canvas尺寸
  handleResize()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// 暴露函数给父组件
defineExpose({
  videoEl,
  captureVideoFrame,
  drawResults
})
</script> 