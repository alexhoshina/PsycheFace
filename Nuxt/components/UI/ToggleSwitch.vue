<template>
    <div class="inline-flex items-center">
      <label class="relative inline-flex items-center cursor-pointer">
        <input 
          type="checkbox" 
          :checked="modelValue" 
          @change="$emit('update:model-value', $event.target.checked)" 
          class="sr-only peer" 
        />
        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-500"></div>
        <span class="ml-3 text-sm font-medium text-gray-700">{{ label }}</span>
      </label>
    </div>
  </template>
  
  <script setup>
  defineProps({
    modelValue: {
      type: Boolean,
      required: true
    },
    label: {
      type: String,
      default: ''
    }
  })
  
  defineEmits(['update:model-value'])
  </script>