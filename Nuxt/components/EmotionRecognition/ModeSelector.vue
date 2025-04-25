<template>
    <div class="flex justify-center mb-8">
      <div class="bg-gray-200 rounded-full p-1 flex">
        <button 
          @click="$emit('update:mode', 'realtime')" 
          :class="[
            'px-6 py-2 text-sm font-medium rounded-full transition-all', 
            modelValue === 'realtime' 
              ? 'bg-blue-500 text-white shadow-md' 
              : 'text-gray-700 hover:bg-gray-300'
          ]"
        >
          实时识别
        </button>
        <button 
          @click="$emit('update:mode', 'upload')" 
          :class="[
            'px-6 py-2 text-sm font-medium rounded-full transition-all', 
            modelValue === 'upload' 
              ? 'bg-blue-500 text-white shadow-md' 
              : 'text-gray-700 hover:bg-gray-300'
          ]"
        >
          上传文件识别
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    modelValue: {
      type: String,
      required: true
    }
  })
  
  defineEmits(['update:mode'])
  </script>