<template>
  <div class="flex justify-center mb-8">
    <div ref="switcherEl" class="bg-gray-200 rounded-full p-1 flex relative">
      <!-- 背景滑块 -->
      <div 
        ref="sliderEl" 
        class="absolute top-1 h-[calc(100%-8px)] bg-blue-500 rounded-full transition-all duration-300 shadow-md"
      ></div>
      
      <button 
        ref="btn1"
        @click="switchMode('realtime')" 
        :class="[
          'px-6 py-2 text-sm font-medium rounded-full transition-colors relative z-10', 
          modelValue === 'realtime' ? 'text-white' : 'text-gray-700 hover:text-gray-900'
        ]"
      >
        实时识别
      </button>
      <button 
        ref="btn2"
        @click="switchMode('upload')" 
        :class="[
          'px-6 py-2 text-sm font-medium rounded-full transition-colors relative z-10', 
          modelValue === 'upload' ? 'text-white' : 'text-gray-700 hover:text-gray-900'
        ]"
      >
        上传文件识别
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { gsap } from 'gsap'

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

// 引用元素
const switcherEl = ref(null)
const sliderEl = ref(null)
const btn1 = ref(null)
const btn2 = ref(null)

// 切换模式
function switchMode(mode) {
  if (mode === props.modelValue) return
  
  emit('update:modelValue', mode)
}

// 动画滑块位置
function animateSlider() {
  if (!sliderEl.value || !btn1.value || !btn2.value) return
  
  const targetBtn = props.modelValue === 'realtime' ? btn1.value : btn2.value
  
  gsap.to(sliderEl.value, {
    width: targetBtn.offsetWidth,
    x: targetBtn.offsetLeft,
    duration: 0.4,
    ease: 'power2.out'
  })
}

// 初始化和监听变化
onMounted(() => {
  // 设置初始位置
  nextTick(() => {
    animateSlider()
  })
})

watch(() => props.modelValue, () => {
  animateSlider()
})
</script>