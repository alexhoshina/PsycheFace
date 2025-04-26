import { ref } from 'vue'

export function useDeviceDetection() {
  const isMobileDevice = ref(false)
  
  // 检测是否为移动设备
  function checkMobileDevice() {
    const userAgent = navigator.userAgent || navigator.vendor || window.opera
    
    // 检测是否为iOS或Android设备
    if (/android/i.test(userAgent) || 
        /iPad|iPhone|iPod/.test(userAgent) || 
        (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) {
      isMobileDevice.value = true
      console.log('检测到移动设备')
    } else {
      isMobileDevice.value = false
      console.log('检测到桌面设备')
    }
  }
  
  return {
    isMobileDevice,
    checkMobileDevice
  }
}