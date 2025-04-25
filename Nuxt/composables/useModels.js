import { ref } from 'vue'
import { fetchModels as apiFetchModels } from '~/services/api'

export function useModels(connectionStatus) {
  const detectorModels = ref([])
  const recognizerModels = ref([])
  const selectedDetector = ref('')
  const selectedRecognizer = ref('')
  
  // 获取可用模型列表
  async function fetchModels() {
    try {
      connectionStatus.value = '正在获取模型列表...'
      
      const { detectorModels: detectors, recognizerModels: recognizers } = await apiFetchModels()
      
      detectorModels.value = detectors
      recognizerModels.value = recognizers
      
      // 默认选择第一个模型
      if (detectorModels.value.length > 0) {
        selectedDetector.value = detectorModels.value[0]
      }
      if (recognizerModels.value.length > 0) {
        selectedRecognizer.value = recognizerModels.value[0]
      }
      
      connectionStatus.value = '模型列表获取成功'
      setTimeout(() => {
        if (connectionStatus.value === '模型列表获取成功') {
          connectionStatus.value = ''
        }
      }, 2000)
    } catch (error) {
      console.error('获取模型失败:', error)
      connectionStatus.value = `错误: 获取模型列表失败 - ${error.message}`
    }
  }
  
  return {
    detectorModels,
    recognizerModels,
    selectedDetector,
    selectedRecognizer,
    fetchModels
  }
}