<template>
  <div class="mb-8 relative">
    <div class="bg-gray-900 rounded-lg overflow-hidden aspect-video relative">
      <div 
        ref="uploadContainer"
        class="absolute inset-0 w-full h-full flex items-center justify-center overflow-hidden"
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
import { ref, onMounted, onUnmounted } from 'vue'
import { gsap } from 'gsap'
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
  }
})

const emit = defineEmits(['file-uploaded'])

// Refs
const canvasEl = ref(null)
const displayCanvas = ref(null)
const uploadedImage = ref(null)
const uploadedFile = ref(null)
const isDragging = ref(false)
const uploadContainer = ref(null)
const dropZone = ref(null)
const dropZoneInner = ref(null)

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
  }
}

// 处理文件选择
function handleFileSelection(file) {
  uploadedFile.value = file
  
  const reader = new FileReader()
  reader.onload = (e) => {
    uploadedImage.value = e.target.result
    
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

// 处理文件上传
function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  
  handleFileSelection(file)
}

// 清除上传的图片
function clearUploadedImage() {
  uploadedImage.value = null
  uploadedFile.value = null
}

// 获取上传的文件
function getUploadedFile() {
  return uploadedFile.value
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

// 绘制结果
function drawResults(results) {
  if (!canvasEl.value || !results.length || !displayCanvas.value || !uploadedImage.value) {
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
    drawFacesOnCanvas(ctx, results, props.showFaceBox, props.showEmotionText, props.showEmoji)
    
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

onMounted(() => {
  // 监听窗口尺寸变化
  window.addEventListener('resize', updateDisplayCanvas)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateDisplayCanvas)
})

// 暴露函数给父组件
defineExpose({
  canvasEl,
  clearUploadedImage,
  getUploadedFile,
  drawResults
})
</script>

<style scoped>
.text-white {
  transition: all 0.3s ease;
}
</style> 