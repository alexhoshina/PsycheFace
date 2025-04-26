<template>
    <div v-if="status" class="mb-4 p-3 rounded-md" :class="statusClass">
      {{ status }}
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    status: {
      type: String,
      default: ''
    }
  })
  
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
  </script>