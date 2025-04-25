<template>
  <div class="mb-8 relative">
    <div class="bg-gray-900 rounded-lg overflow-hidden aspect-video relative">
      <!-- 视频显示 -->
      <video
        v-show="mode === 'realtime'"
        ref="videoEl"
        autoplay
        muted
        playsinline
        class="w-full h-full object-cover"
      ></video>
      
      <!-- 上传图片显示 -->
      <div v-show="mode === 'upload'" class="w-full h-full flex items-center justify-center">
        <img 
          v-if="uploadedImage" 
          :src="uploadedImage" 
          class="max-w-full max-h-full object-contain" 
          ref="imageEl"
        />
        <div 
          v-else 
          class="text-white text-center p-8"
          @dragover.prevent="onDragOver"
          @dragleave.prevent="onDragLeave"
          @drop.prevent="onDrop"
          :class="{'bg-blue-800/30': isDragging}"
        >
          <div class="border-2 border-dashed border-gray-400 rounded-lg p-8" :class="{'border-blue-400': isDragging}">
            <p class="mb-4">拖放图片到这里或</p>
            <label class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg cursor-pointer">
              选择文件
              <input type="file" accept="image/*" class="hidden" @change="handleFileUpload" />
            </label>
          </div>
        </div>
      </div>
      
      <!-- 人脸检测框和表情标签叠加层 -->
      <canvas
        v-show="isRecognizing || uploadedImageProcessed"
        ref="canvasEl"
        class="absolute top-0 left-0 w-full h-full"
      ></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { drawFacesOnCanvas } from '~/utils/canvasUtils'

// Props
const props = defineProps({
  mode: {
    type: String,
    required: true
  },
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
  }
})

const emit = defineEmits(['file-uploaded'])

// Refs
const videoEl = ref(null)
const canvasEl = ref(null)
const imageEl = ref(null)
const uploadedImage = ref(null)
const uploadedFile = ref(null)
const uploadedImageProcessed = ref(false)
const isDragging = ref(false)

// 拖拽处理
function onDragOver(event) {
  isDragging.value = true
}

function onDragLeave(event) {
  isDragging.value = false
}

function onDrop(event) {
  isDragging.value = false
  const files = event.dataTransfer.files
  
  if (files.length > 0 && files[0].type.startsWith('image/')) {
    handleFileSelection(files[0])
  }
}

// 处理上传图片
function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  
  handleFileSelection(file)
}

function handleFileSelection(file) {
  uploadedFile.value = file
  
  const reader = new FileReader()
  reader.onload = (e) => {
    uploadedImage.value = e.target.result
    uploadedImageProcessed.value = false
    
    // 通知父组件已上传文件
    emit('file-uploaded', file)
  }
  reader.readAsDataURL(file)
}

// 清除上传的图片
function clearUploadedImage() {
  uploadedImage.value = null
  uploadedFile.value = null
  uploadedImageProcessed.value = false
}

// 获取上传的文件
function getUploadedFile() {
  return uploadedFile.value
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

// 捕获上传的图片
function captureUploadedImage() {
  if (!imageEl.value || !uploadedImage.value) return null
  
  const canvas = document.createElement('canvas')
  const context = canvas.getContext('2d')
  canvas.width = imageEl.value.naturalWidth
  canvas.height = imageEl.value.naturalHeight
  context.drawImage(imageEl.value, 0, 0, canvas.width, canvas.height)
  
  return canvas
}

// 绘制识别结果
function drawResults(results, showFaceBox, showEmotionText, showEmoji) {
  if (!canvasEl.value || !results.length) return
  
  const canvas = canvasEl.value
  const ctx = canvas.getContext('2d')
  
  // 确保canvas大小与视频/图片大小一致
  if (props.mode === 'realtime' && videoEl.value) {
    canvas.width = videoEl.value.videoWidth
    canvas.height = videoEl.value.videoHeight
  } else if (props.mode === 'upload' && imageEl.value) {
    canvas.width = imageEl.value.naturalWidth
    canvas.height = imageEl.value.naturalHeight
  }
  
  // 清除之前的绘制
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  // 绘制人脸框和表情
  drawFacesOnCanvas(ctx, results, showFaceBox, showEmotionText, showEmoji)
  
  // 如果是上传图片模式，标记为已处理
  if (props.mode === 'upload') {
    uploadedImageProcessed.value = true
  }
}

// 设置Canvas大小
function setupCanvas() {
  if (canvasEl.value) {
    const container = canvasEl.value.parentElement
    canvasEl.value.width = container.clientWidth
    canvasEl.value.height = container.clientHeight
  }
}

onMounted(() => {
  setupCanvas()
  
  // 监听窗口尺寸变化
  window.addEventListener('resize', setupCanvas)
})

// 清除事件监听
onUnmounted(() => {
  window.removeEventListener('resize', setupCanvas)
})

// 暴露函数给父组件
defineExpose({
  videoEl,
  canvasEl,
  captureVideoFrame,
  captureUploadedImage,
  drawResults,
  clearUploadedImage,
  getUploadedFile
})
</script>

<style scoped>
/* 添加过渡效果 */
.text-white {
  transition: all 0.3s ease;
}
</style>