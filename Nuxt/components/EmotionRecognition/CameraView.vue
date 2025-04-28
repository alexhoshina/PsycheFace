<template>
  <div class="mb-8 relative">
    <div class="bg-gray-900 rounded-lg overflow-hidden aspect-video relative">
      <!-- 视频显示 -->
      <div 
        ref="videoContainer" 
        class="absolute inset-0 w-full h-full"
        :class="{'opacity-0': mode !== 'realtime'}"
      >
        <video
          ref="videoEl"
          autoplay
          muted
          playsinline
          class="w-full h-full object-cover"
        ></video>
      </div>
      
      <!-- 上传图片显示 -->
      <div 
        ref="uploadContainer"
        class="absolute inset-0 w-full h-full flex items-center justify-center"
        :class="{'opacity-0': mode !== 'upload'}"
      >
        <img 
          v-if="uploadedImage" 
          :src="uploadedImage" 
          class="max-w-full max-h-full object-contain" 
          ref="imageEl"
        />
        <div 
          v-else 
          class="text-white text-center p-8 w-full h-full flex items-center justify-center"
          @dragover.prevent="onDragOver"
          @dragleave.prevent="onDragLeave"
          @drop.prevent="onDrop"
          ref="dropZone"
        >
          <div 
            class="border-2 border-dashed border-gray-400 rounded-lg p-12 transition-all duration-300 transform"
            :class="{'border-blue-400 scale-105 bg-blue-800/20': isDragging}"
            ref="dropZoneInner"
          >
            <p class="mb-4">拖放图片到这里或</p>
            <label class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg cursor-pointer inline-block">
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
import { ref, onMounted, watch, nextTick } from 'vue'
import { gsap } from 'gsap'
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
  },
  mediaStream: {
    //type: MediaStream,
    default: null
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

// 动画容器
const videoContainer = ref(null)
const uploadContainer = ref(null)
const dropZone = ref(null)
const dropZoneInner = ref(null)

// 处理模式变化的动画
watch(() => props.mode, (newMode, oldMode) => {
  if (!videoContainer.value || !uploadContainer.value) return
  
  // 淡出当前模式
  const fadeOut = newMode === 'realtime' ? uploadContainer.value : videoContainer.value
  const fadeIn = newMode === 'realtime' ? videoContainer.value : uploadContainer.value
  
  gsap.to(fadeOut, {
    opacity: 0,
    duration: 0.3,
    ease: 'power2.out'
  })
  
  gsap.to(fadeIn, {
    opacity: 1,
    duration: 0.3,
    delay: 0.1,
    ease: 'power2.out'
  })
  
  // 如果切换到上传模式，添加上传区域动画
  if (newMode === 'upload' && dropZoneInner.value) {
    gsap.fromTo(dropZoneInner.value, 
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.5, delay: 0.2, ease: 'back.out' }
    )
  }
})

// 拖拽处理动画
function onDragOver(event) {
  isDragging.value = true
  if (dropZoneInner.value) {
    gsap.to(dropZoneInner.value, {
      scale: 1.05,
      boxShadow: "0 0 30px rgba(59, 130, 246, 0.3)",
      duration: 0.2
    })
  }
}

function onDragLeave(event) {
  isDragging.value = false
  if (dropZoneInner.value) {
    gsap.to(dropZoneInner.value, {
      scale: 1,
      boxShadow: "none",
      duration: 0.2
    })
  }
}

function onDrop(event) {
  isDragging.value = false
  
  if (dropZoneInner.value) {
    gsap.to(dropZoneInner.value, {
      scale: 1,
      boxShadow: "none",
      duration: 0.2
    })
  }
  
  const files = event.dataTransfer.files
  
  if (files.length > 0 && files[0].type.startsWith('image/')) {
    handleFileSelection(files[0])
    
    // 添加文件上传成功动画
    gsap.fromTo(dropZoneInner.value,
      { scale: 0.95, opacity: 0.8 },
      { 
        scale: 1, 
        opacity: 1, 
        duration: 0.4,
        ease: "elastic.out(1, 0.5)" 
      }
    )
  }
}

// 处理上传图片时的动画
function handleFileSelection(file) {
  uploadedFile.value = file
  
  const reader = new FileReader()
  reader.onload = (e) => {
    // 创建一个图像预加载对象
    const img = new Image()
    img.onload = () => {
      // 图像加载完成后执行动画
      uploadedImage.value = e.target.result
      uploadedImageProcessed.value = false
      
      // 通知父组件已上传文件
      emit('file-uploaded', file)
      
      nextTick(() => {
        if (imageEl.value) {
          // 图像显示动画
          gsap.fromTo(imageEl.value,
            { opacity: 0, scale: 0.9 },
            { 
              opacity: 1, 
              scale: 1, 
              duration: 0.5,
              ease: "power2.out" 
            }
          )
        }
      })
    }
    
    img.src = e.target.result
  }
  reader.readAsDataURL(file)
}
// 处理上传图片
function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  
  handleFileSelection(file)
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

// 设置Canvas大小
function setupCanvas() {
  if (canvasEl.value) {
    const container = canvasEl.value.parentElement
    canvasEl.value.width = container.clientWidth
    canvasEl.value.height = container.clientHeight
  }
}

// 绘制识别结果时添加动画
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
  
  // 使用动画显示canvas
  gsap.fromTo(canvas,
    { opacity: 0 },
    { opacity: 1, duration: 0.3, ease: "power1.out" }
  )
  
  // 绘制人脸框和表情
  drawFacesOnCanvas(ctx, results, showFaceBox, showEmotionText, showEmoji)
  
  // 如果是上传图片模式，标记为已处理
  if (props.mode === 'upload') {
    uploadedImageProcessed.value = true
  }
}

// 监听媒体流变化
watch(() => props.mediaStream, (newStream) => {
  if (newStream && videoEl.value) {
    videoEl.value.srcObject = newStream
  }
})

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