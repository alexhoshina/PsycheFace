import { ref } from 'vue'
import { createWebSocketConnection, sendImageData } from '~/services/api'

export function useWebSocket(
  selectedDetector, 
  selectedRecognizer, 
  connectionStatus, 
  onMessage
) {
  const ws = ref(null)
  const isFrameProcessing = ref(false)
  
  // 开启/关闭WebSocket连接，返回一个Promise，连接成功时resolve
  function initWebSocket() {
    return new Promise((resolve, reject) => {
      closeWebSocket()
      
      connectionStatus.value = '正在连接WebSocket...'
      
      try {
        ws.value = createWebSocketConnection(
          selectedDetector.value,
          selectedRecognizer.value,
          {
            onOpen: () => {
              console.log('WebSocket连接成功')
              connectionStatus.value = 'WebSocket已连接，开始识别'
              resolve() // 连接成功，resolve Promise
            },
            onMessage: (data) => {
              onMessage(data)
              // 收到消息后，标记帧处理完成，可以处理下一帧
              isFrameProcessing.value = false
            },
            onError: (error) => {
              console.error('WebSocket错误:', error)
              connectionStatus.value = '错误: WebSocket连接失败'
              isFrameProcessing.value = false
              reject(error) // 连接错误，reject Promise
            },
            onClose: () => {
              console.log('WebSocket连接关闭')
              if (connectionStatus.value.includes('正在连接')) {
                connectionStatus.value = '错误: WebSocket连接关闭'
              }
              isFrameProcessing.value = false
            }
          }
        )
        
        // 设置超时，如果5秒内没有连接成功，则reject
        setTimeout(() => {
          if (ws.value && ws.value.readyState !== WebSocket.OPEN) {
            connectionStatus.value = '错误: WebSocket连接超时'
            closeWebSocket()
            reject(new Error('WebSocket连接超时'))
          }
        }, 5000)
      } catch (error) {
        connectionStatus.value = `错误: ${error.message}`
        reject(error)
      }
    })
  }
  
  function closeWebSocket() {
    if (ws.value) {
      if (ws.value.readyState === WebSocket.OPEN || ws.value.readyState === WebSocket.CONNECTING) {
        ws.value.close()
      }
      ws.value = null
    }
  }
  
  // 发送视频帧
  async function sendFrame(canvas) {
    if (!ws.value || ws.value.readyState !== WebSocket.OPEN || isFrameProcessing.value) return
    
    isFrameProcessing.value = true
    
    try {
      await sendImageData(ws.value, canvas)
      console.log('已发送图像')
    } catch (error) {
      console.error('发送数据失败:', error)
      isFrameProcessing.value = false
    }
  }
  
  return {
    ws,
    isFrameProcessing,
    initWebSocket,
    closeWebSocket,
    sendFrame
  }
}