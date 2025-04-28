<template>
  <div 
    v-if="status" 
    class="mb-4 p-3 rounded-md overflow-hidden" 
    :class="statusClass"
    ref="statusBar"
  >
    {{ status }}
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { gsap } from 'gsap'

const props = defineProps({
  status: {
    type: String,
    default: ''
  }
})

const statusBar = ref(null)
const prevStatus = ref('')

const statusClass = computed(() => {
  if (props.status.includes('错误') || props.status.includes('失败')) {
    return 'bg-red-100 text-red-800'
  } else if (props.status.includes('连接中') || props.status.includes('正在')) {
    return 'bg-yellow-100 text-yellow-800'
  } else if (props.status.includes('已连接') || props.status.includes('成功')) {
    return 'bg-green-100 text-green-800'
  } else if (props.status.includes('警告')) {
    return 'bg-orange-100 text-orange-800'
  }
  return 'bg-gray-100 text-gray-800'
})

// 监听状态变化
watch(() => props.status, (newStatus, oldStatus) => {
  if (!statusBar.value) return
  
  if (newStatus && !oldStatus) {
    // 显示动画
    gsap.fromTo(statusBar.value,
      { y: -50, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.3, ease: "back.out" }
    )
  } else if (oldStatus && !newStatus) {
    // 隐藏动画
    gsap.to(statusBar.value, {
      y: -50, 
      opacity: 0, 
      duration: 0.3,
      ease: "power2.in"
    })
  } else if (newStatus !== oldStatus) {
    // 状态更新动画
    const timeline = gsap.timeline()
    
    timeline.to(statusBar.value, {
      opacity: 0,
      y: -10,
      duration: 0.15,
      ease: "power1.in",
      onComplete: () => {
        prevStatus.value = newStatus
      }
    })
    
    timeline.fromTo(statusBar.value,
      { opacity: 0, y: 10 },
      { opacity: 1, y: 0, duration: 0.2, ease: "power1.out" }
    )
  }
}, { immediate: true })
</script>