<!-- components/Camera.vue -->
<template>
    <div class="relative w-full h-full">
      <video
        ref="videoEl"
        autoplay
        muted
        playsinline
        class="w-full h-full object-cover"
      ></video>
      
      <div v-if="!isStreamActive" class="absolute inset-0 flex items-center justify-center bg-black/70 text-white">
        <div class="text-center">
          <p class="mb-2">摄像头未启动</p>
          <button @click="initCamera" class="px-3 py-1 bg-blue-500 rounded text-sm">
            启动摄像头
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted, computed } from 'vue'
  
  const props = defineProps({
    deviceId: {
      type: String,
      default: ''
    },
    autoStart: {
      type: Boolean,
      default: true
    }
  })
  
  const emit = defineEmits(['stream-ready', 'stream-error'])
  
  const videoEl = ref(null)
  const mediaStream = ref(null)
  
  // 计算属性，检查流是否活跃
  const isStreamActive = computed(() => {
    return mediaStream.value && 
           mediaStream.value.active && 
           videoEl.value && 
           videoEl.value.srcObject === mediaStream.value
  })
  
  // 初始化摄像头
  async function initCamera() {
    try {
      // 停止之前的流
      stopStream()
      
      // 设置约束条件
      const constraints = {
        video: props.deviceId 
          ? { deviceId: { exact: props.deviceId } } 
          : true
      }
      
      console.log('请求摄像头权限:', constraints)
      
      // 获取媒体流
      const stream = await navigator.mediaDevices.getUserMedia(constraints)
      mediaStream.value = stream
      
      console.log('成功获取摄像头流:', stream)
      
      // 手动设置到视频元素
      if (videoEl.value) {
        videoEl.value.srcObject = stream
        console.log('已设置视频源')
        
        // 等待视频加载
        await new Promise((resolve) => {
          const onLoaded = () => {
            videoEl.value.removeEventListener('loadeddata', onLoaded)
            console.log('视频数据已加载, 尺寸:', videoEl.value.videoWidth, 'x', videoEl.value.videoHeight)
            resolve()
          }
          
          if (videoEl.value.readyState >= 2) {
            console.log('视频已经有数据')
            resolve()
          } else {
            videoEl.value.addEventListener('loadeddata', onLoaded)
          }
        })
        
        emit('stream-ready', stream)
      }
    } catch (error) {
      console.error('摄像头初始化失败:', error)
      emit('stream-error', error)
    }
  }
  
  // 停止流
  function stopStream() {
    if (mediaStream.value) {
      mediaStream.value.getTracks().forEach(track => track.stop())
      mediaStream.value = null
    }
    
    if (videoEl.value) {
      videoEl.value.srcObject = null
    }
  }
  
  // 捕获当前帧
  function captureFrame() {
    if (!videoEl.value || videoEl.value.readyState < 2) return null
    
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    canvas.width = videoEl.value.videoWidth
    canvas.height = videoEl.value.videoHeight
    ctx.drawImage(videoEl.value, 0, 0)
    
    return canvas
  }
  
  // 生命周期钩子
  onMounted(() => {
    if (props.autoStart) {
      initCamera()
    }
  })
  
  onUnmounted(() => {
    stopStream()
  })
  
  // 暴露方法
  defineExpose({
    videoEl,
    initCamera,
    stopStream,
    captureFrame,
    isStreamActive
  })
  </script>