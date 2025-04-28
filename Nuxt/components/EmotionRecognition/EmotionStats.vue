<template>
  <div class="bg-white p-6 rounded-lg shadow-md" ref="statsContainer">
    <h3 class="text-lg font-medium text-gray-900 mb-4">识别结果统计</h3>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div 
        v-for="(count, code) in emotionStats" 
        :key="code" 
        class="bg-gray-100 p-4 rounded-lg text-center"
        :ref="el => statCards[code] = el"
      >
        <div class="text-2xl mb-1">{{ emotionLabels[code][1] }}</div>
        <div class="text-sm text-gray-600">{{ emotionLabels[code][0] }}</div>
        <div class="text-xl font-bold mt-2" :ref="el => countElements[code] = el">{{ count }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, reactive } from 'vue'
import { gsap } from 'gsap'
import { emotionLabels } from '~/utils/emotions'

const props = defineProps({
  emotionStats: {
    type: Object,
    required: true
  }
})

// 用于动画的引用
const statsContainer = ref(null)
const statCards = reactive({})
const countElements = reactive({})
const prevStats = ref({...props.emotionStats})

// 入场动画
onMounted(() => {
  if (statsContainer.value) {
    gsap.fromTo(statsContainer.value,
      { y: 30, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.5, delay: 0.2, ease: "power2.out" }
    )
    
    // 卡片依次显示
    const cards = Object.values(statCards)
    if (cards.length) {
      gsap.fromTo(cards,
        { scale: 0.8, opacity: 0 },
        { 
          scale: 1, 
          opacity: 1, 
          duration: 0.4, 
          stagger: 0.05, 
          delay: 0.4,
          ease: "back.out(1.7)" 
        }
      )
    }
  }
})

// 数值变化动画
watch(() => props.emotionStats, (newStats) => {
  Object.entries(newStats).forEach(([code, count]) => {
    const prevCount = prevStats.value[code] || 0
    
    if (count !== prevCount && countElements[code]) {
      // 数字变化动画
      gsap.to(countElements[code], {
        innerHTML: count,
        duration: 0.5,
        snap: { innerHTML: 1 }, // 确保数字是整数
        ease: "power2.inOut"
      })
      
      // 卡片闪烁效果
      if (statCards[code] && count > prevCount) {
        gsap.fromTo(statCards[code],
          { backgroundColor: "rgba(59, 130, 246, 0.2)" },
          { 
            backgroundColor: "rgba(243, 244, 246, 1)", 
            duration: 0.8,
            ease: "power2.out" 
          }
        )
        
        gsap.fromTo(statCards[code],
          { scale: 1.05 },
          { scale: 1, duration: 0.4, ease: "back.out" }
        )
      }
    }
  })
  
  prevStats.value = {...newStats}
}, { deep: true })
</script>