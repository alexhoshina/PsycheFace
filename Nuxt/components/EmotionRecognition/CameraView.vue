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
          >
            <p class="mb-4">拖放图片到这里或</p>
            <label class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg cursor-pointer">
              选择文件
              <input type="file" accept="image/*" class="hidden" @change="handleFileUpload" />
            </label>
          </div>
        </div>
        
        <!-- 人脸检测框和表情标签叠加层 -->
        <canvas
          v-show="isRecognizing"
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
  
  // Refs
  const videoEl = ref(null)
  const canvasEl = ref(null)
  const imageEl = ref(null)
  const uploadedImage = ref(null)
  
  // 处理上传图片
  function handleFileUpload(event) {
    const file = event.target.files[0]
    if (!file) return
    
    const reader = new FileReader()
    reader.onload = (e) => {
      uploadedImage.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
  
  // 清除上传的图片
  function clearUploadedImage() {
    uploadedImage.value = null
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
  
  // 暴露函数给父组件
  defineExpose({
    videoEl,
    canvasEl,
    captureVideoFrame,
    captureUploadedImage,
    drawResults,
    clearUploadedImage
  })
  </script>