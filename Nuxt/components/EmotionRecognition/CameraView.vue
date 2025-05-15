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
        class="absolute inset-0 w-full h-full flex items-center justify-center overflow-hidden"
        :class="{'opacity-0': mode !== 'upload'}"
      >
        <template v-if="uploadedImage">
          <div class="relative w-full h-full flex items-center justify-center">
            <!-- 显示用的canvas -->
            <canvas
              ref="displayCanvas"
              class="max-w-full max-h-full object-contain"
            ></canvas>
            <!-- 绘制用的canvas（隐藏） -->
            <canvas
              ref="canvasEl"
              class="hidden"
            ></canvas>
          </div>
        </template>
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

// 添加displayCanvas的ref
const displayCanvas = ref(null)

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
    console.log('文件读取完成，开始加载图片')
    uploadedImage.value = e.target.result
    uploadedImageProcessed.value = false
    
    // 通知父组件已上传文件
    emit('file-uploaded', file)
    
    nextTick(() => {
      if (displayCanvas.value) {
        // 更新显示canvas
        updateDisplayCanvas()
        
        // 图像显示动画
        gsap.fromTo(displayCanvas.value,
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
  if (!displayCanvas.value || !uploadedImage.value) return null
  
  const canvas = document.createElement('canvas')
  const context = canvas.getContext('2d')
  const displayCtx = displayCanvas.value.getContext('2d')
  
  // 创建临时图片对象
  const img = new Image()
  img.onload = () => {
    canvas.width = img.naturalWidth
    canvas.height = img.naturalHeight
    context.drawImage(img, 0, 0, canvas.width, canvas.height)
  }
  
  img.src = uploadedImage.value
  return canvas
}

// 设置Canvas大小
function setupCanvas() {
  if (!canvasEl.value) return
  
  if (props.mode === 'realtime' && videoEl.value) {
    const container = canvasEl.value.parentElement
    canvasEl.value.width = container.clientWidth
    canvasEl.value.height = container.clientHeight
  } else if (props.mode === 'upload' && imageEl.value) {
    updateCanvasSize()
  }
}

// 更新Canvas大小以匹配图片
function updateCanvasSize() {
  if (!canvasEl.value || !imageEl.value) {
    console.log('updateCanvasSize: canvas或image元素不存在', {
      canvas: canvasEl.value,
      image: imageEl.value
    })
    return
  }
  
  console.log('更新Canvas大小前:', {
    canvasWidth: canvasEl.value.width,
    canvasHeight: canvasEl.value.height,
    imageNaturalWidth: imageEl.value.naturalWidth,
    imageNaturalHeight: imageEl.value.naturalHeight,
    imageClientWidth: imageEl.value.clientWidth,
    imageClientHeight: imageEl.value.clientHeight
  })
  
  canvasEl.value.width = imageEl.value.naturalWidth
  canvasEl.value.height = imageEl.value.naturalHeight
  
  console.log('更新Canvas大小后:', {
    canvasWidth: canvasEl.value.width,
    canvasHeight: canvasEl.value.height
  })
}

// 更新显示canvas
function updateDisplayCanvas() {
  if (!displayCanvas.value || !uploadedImage.value) return
  
  const displayCtx = displayCanvas.value.getContext('2d')
  const container = displayCanvas.value.parentElement
  
  // 创建临时图片对象
  const img = new Image()
  img.onload = () => {
    // 设置显示canvas的尺寸为容器大小
    displayCanvas.value.width = container.clientWidth
    displayCanvas.value.height = container.clientHeight
    
    // 清除画布
    displayCtx.clearRect(0, 0, displayCanvas.value.width, displayCanvas.value.height)
    
    // 计算图片的显示尺寸和位置
    const imgRatio = img.naturalWidth / img.naturalHeight
    const containerRatio = container.clientWidth / container.clientHeight
    
    let drawWidth, drawHeight, offsetX, offsetY
    
    if (imgRatio > containerRatio) {
      // 图片更宽，以宽度为基准
      drawWidth = container.clientWidth
      drawHeight = drawWidth / imgRatio
      offsetX = 0
      offsetY = (container.clientHeight - drawHeight) / 2
    } else {
      // 图片更高，以高度为基准
      drawHeight = container.clientHeight
      drawWidth = drawHeight * imgRatio
      offsetX = (container.clientWidth - drawWidth) / 2
      offsetY = 0
    }
    
    // 绘制图片
    displayCtx.drawImage(img, offsetX, offsetY, drawWidth, drawHeight)
  }
  
  img.src = uploadedImage.value
}

// 修改drawResults函数
function drawResults(results, showFaceBox, showEmotionText, showEmoji) {
  if (!canvasEl.value || !results.length || !displayCanvas.value || !uploadedImage.value) {
    console.log('drawResults: canvas不存在或没有结果', {
      canvas: canvasEl.value,
      displayCanvas: displayCanvas.value,
      resultsLength: results.length,
      hasImage: !!uploadedImage.value
    })
    return
  }
  
  const canvas = canvasEl.value
  const ctx = canvas.getContext('2d')
  const displayCtx = displayCanvas.value.getContext('2d')
  
  // 创建临时图片对象
  const img = new Image()
  img.onload = () => {
    // 设置绘制canvas为图片原始尺寸
    canvas.width = img.naturalWidth
    canvas.height = img.naturalHeight
    
    // 清除之前的绘制
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    // 绘制人脸框和表情
    drawFacesOnCanvas(ctx, results, showFaceBox, showEmotionText, showEmoji)
    
    // 将绘制结果复制到显示canvas
    const container = displayCanvas.value.parentElement
    const imgRatio = img.naturalWidth / img.naturalHeight
    const containerRatio = container.clientWidth / container.clientHeight
    
    let drawWidth, drawHeight, offsetX, offsetY
    
    if (imgRatio > containerRatio) {
      drawWidth = container.clientWidth
      drawHeight = drawWidth / imgRatio
      offsetX = 0
      offsetY = (container.clientHeight - drawHeight) / 2
    } else {
      drawHeight = container.clientHeight
      drawWidth = drawHeight * imgRatio
      offsetX = (container.clientWidth - drawWidth) / 2
      offsetY = 0
    }
    
    // 将绘制结果复制到显示canvas
    displayCtx.drawImage(canvas, offsetX, offsetY, drawWidth, drawHeight)
  }
  
  img.src = uploadedImage.value
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
  window.addEventListener('resize', () => {
    setupCanvas()
    updateDisplayCanvas()
  })
})

// 清除事件监听
onUnmounted(() => {
  window.removeEventListener('resize', () => {
    setupCanvas()
    updateDisplayCanvas()
  })
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