import { ref } from 'vue'

export function useCamera(connectionStatus, isMobileDevice) {
  const mediaStream = ref(null)
  const availableCameras = ref([])
  const selectedCamera = ref('')
  const cameraFacing = ref('front') // 默认使用前置摄像头
  
  // 获取摄像头列表
  async function getAvailableCameras() {
    try {
      // 检查MediaDevices API是否可用
      if (!navigator.mediaDevices) {
        console.warn('MediaDevices API不可用，无法列出摄像头。这在非HTTPS连接或某些浏览器中是正常的。')
        return
      }
      
      if (!isMobileDevice.value) {
        try {
          // 先请求权限
          await navigator.mediaDevices.getUserMedia({ video: true })
          
          // 获取所有视频输入设备
          const devices = await navigator.mediaDevices.enumerateDevices()
          const videoDevices = devices.filter(device => device.kind === 'videoinput')
          availableCameras.value = videoDevices
          
          // 如果有可用摄像头，设置默认选择
          if (videoDevices.length > 0) {
            selectedCamera.value = videoDevices[0].deviceId
          }
          
          console.log('可用摄像头:', videoDevices)
        } catch (err) {
          console.warn('无法枚举摄像头设备:', err)
        }
      }
    } catch (error) {
      console.error('检查摄像头时出错:', error)
    }
  }
  
  // 处理摄像头切换
  async function handleCameraChange(deviceId) {
    selectedCamera.value = deviceId
    
    if (mediaStream.value) {
      // 停止当前摄像头
      releaseCamera()
      
      connectionStatus.value = '正在切换摄像头...'
      await setupCamera()
      connectionStatus.value = '摄像头已切换'
    }
  }
  
  // 切换前置/后置摄像头
  async function toggleCamera(facing) {
    if (facing === cameraFacing.value) return
    
    cameraFacing.value = facing
    connectionStatus.value = `正在切换到${facing === 'front' ? '前置' : '后置'}摄像头...`
    
    if (mediaStream.value) {
      releaseCamera()
      await setupCamera()
    }
  }
  
  // 摄像头处理逻辑
  async function setupCamera() {
    try {
      // 释放之前的摄像头资源
      releaseCamera()
      
      // 首先检查MediaDevices API是否可用
      if (!navigator.mediaDevices) {
        throw new Error('此浏览器不支持摄像头访问(MediaDevices API不可用)。请尝试使用最新版Chrome或Safari，并确保通过HTTPS连接访问。');
      }
      
      // 检查getUserMedia方法是否可用
      if (!navigator.mediaDevices.getUserMedia) {
        throw new Error('此浏览器不支持摄像头访问(getUserMedia不可用)。请尝试使用最新版Chrome或Safari。');
      }
      
      let constraints = {}
      
      if (isMobileDevice.value) {
        // 移动设备使用前置/后置摄像头
        constraints = {
          video: {
            facingMode: cameraFacing.value === 'front' ? 'user' : 'environment',
            width: { ideal: 1280 },
            height: { ideal: 720 }
          }
        }
        console.log(`使用${cameraFacing.value === 'front' ? '前置' : '后置'}摄像头`)
      } else {
        // 桌面设备使用指定的摄像头ID
        constraints = {
          video: selectedCamera.value 
            ? { deviceId: { exact: selectedCamera.value } } 
            : true
        }
      }
      
      console.log('使用摄像头配置:', constraints)
      
      try {
        mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)
      } catch (err) {
        // 如果指定配置失败，尝试使用最简单的配置
        console.error('使用指定配置获取摄像头失败，尝试默认配置:', err)
        mediaStream.value = await navigator.mediaDevices.getUserMedia({ video: true })
      }
      
      return mediaStream.value
    } catch (error) {
      console.error('设置摄像头错误:', error)
      let errorMessage = '无法访问摄像头，请检查权限设置'
      
      // 提供更具体的错误信息
      if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
        errorMessage = '未检测到摄像头设备。请确保您的设备有摄像头并已启用。'
      } else if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        errorMessage = '摄像头访问被拒绝。请在您的浏览器设置中允许访问摄像头。'
      } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
        errorMessage = '无法访问摄像头，摄像头可能被其他应用占用。'
      } else if (error.name === 'OverconstrainedError' || error.name === 'ConstraintNotSatisfiedError') {
        errorMessage = '摄像头不满足要求的配置，请尝试其他摄像头。'
      } else if (error.name === 'TypeError' || error.message.includes('undefined')) {
        errorMessage = '浏览器不支持摄像头访问。请确保使用最新版的浏览器并通过HTTPS连接访问。'
      } else {
        errorMessage = `摄像头访问错误: ${error.message || error}`
      }
      
      // 检查协议
      if (window.location.protocol === 'http:' && window.location.hostname !== 'localhost') {
        errorMessage += '。注意: 大多数浏览器需要HTTPS连接才能访问摄像头！'
      }
      
      connectionStatus.value = `错误: ${errorMessage}`
      throw error
    }
  }
  
  function releaseCamera() {
    if (mediaStream.value) {
      mediaStream.value.getTracks().forEach(track => track.stop())
      mediaStream.value = null
    }
  }
  
  return {
    mediaStream,
    availableCameras,
    selectedCamera,
    cameraFacing,
    setupCamera,
    releaseCamera,
    getAvailableCameras,
    handleCameraChange,
    toggleCamera
  }
}