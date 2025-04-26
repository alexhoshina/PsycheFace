<template>
    <div class="bg-white p-6 rounded-lg shadow-md">
      <h3 class="text-lg font-medium text-gray-900 mb-4">识别结果统计</h3>
      
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div 
          v-for="(count, code) in emotionStats" 
          :key="code" 
          class="bg-gray-100 p-4 rounded-lg text-center"
        >
          <div class="text-2xl mb-1">{{ emotionLabels[code][1] }}</div>
          <div class="text-sm text-gray-600">{{ emotionLabels[code][0] }}</div>
          <div class="text-xl font-bold mt-2">{{ count }}</div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { emotionLabels } from '~/utils/emotions'
  
  defineProps({
    emotionStats: {
      type: Object,
      required: true
    }
  })
  </script>