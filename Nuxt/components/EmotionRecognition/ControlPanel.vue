<template>
    <div class="mb-8 bg-white p-6 rounded-lg shadow-md">
      <h3 class="text-lg font-medium text-gray-900 mb-4">功能选项</h3>
      
      <!-- 模型选择 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">人脸定位模型</label>
          <select 
            :value="selectedDetector" 
            @input="$emit('update:selected-detector', $event.target.value)" 
            class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="isRecognizing"
          >
            <option v-for="model in detectorModels" :key="model" :value="model">
              {{ model }}
            </option>
          </select>
        </div>
  
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">表情识别模型</label>
          <select 
            :value="selectedRecognizer"
            @input="$emit('update:selected-recognizer', $event.target.value)"
            class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="isRecognizing"
          >
            <option v-for="model in recognizerModels" :key="model" :value="model">
              {{ model }}
            </option>
          </select>
        </div>
      </div>
      
      <!-- 摄像头控制 -->
      <div class="mb-4" v-if="mode === 'realtime'">
        <div class="flex flex-col space-y-3">
          <!-- 移动设备前后摄像头切换 -->
          <div v-if="isMobileDevice" class="flex justify-between items-center">
            <label class="block text-sm font-medium text-gray-700">选择摄像头</label>
            <div class="flex space-x-2">
              <button 
                @click="$emit('toggle-camera', 'front')" 
                :class="[
                  'px-3 py-1 text-sm rounded transition-colors', 
                  cameraFacing === 'front' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-200 text-gray-800'
                ]"
                :disabled="isRecognizing"
              >
                前置
              </button>
              <button 
                @click="$emit('toggle-camera', 'back')" 
                :class="[
                  'px-3 py-1 text-sm rounded transition-colors', 
                  cameraFacing === 'back' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-200 text-gray-800'
                ]"
                :disabled="isRecognizing"
              >
                后置
              </button>
            </div>
          </div>
          
          <!-- 桌面设备摄像头选择 -->
          <div v-else-if="availableCameras.length > 0" class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">选择摄像头</label>
            <select 
              :value="selectedCamera"
              @input="$emit('update:selected-camera', $event.target.value)"
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              :disabled="isRecognizing"
            >
              <option v-for="camera in availableCameras" :key="camera.deviceId" :value="camera.deviceId">
                {{ camera.label || `摄像头 ${availableCameras.indexOf(camera) + 1}` }}
              </option>
            </select>
          </div>
        </div>
      </div>
      
      <!-- 控制按钮和开关 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <button 
            @click="$emit('toggle-recognition')" 
            class="w-full px-4 py-3 rounded-lg text-white font-medium transition-colors"
            :class="isRecognizing ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'"
          >
            {{ isRecognizing ? '暂停识别' : '开始识别' }}
          </button>
        </div>
        
        <div class="flex flex-col space-y-3">
          <!-- 显示选项开关 - 使用组件 -->
          <toggle-switch 
            :model-value="showFaceBox" 
            @update:model-value="$emit('update:show-face-box', $event)"
            label="显示人脸框"
          />
          
          <toggle-switch 
            :model-value="showEmotionText" 
            @update:model-value="$emit('update:show-emotion-text', $event)"
            label="显示表情名称"
          />
          
          <toggle-switch 
            :model-value="showEmoji" 
            @update:model-value="$emit('update:show-emoji', $event)"
            label="显示Emoji"
          />
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue'
  import ToggleSwitch from '../UI/ToggleSwitch.vue'
  
  defineProps({
    mode: String,
    detectorModels: Array,
    recognizerModels: Array,
    selectedDetector: String,
    selectedRecognizer: String,
    isRecognizing: Boolean,
    showFaceBox: Boolean,
    showEmotionText: Boolean,
    showEmoji: Boolean,
    isMobileDevice: Boolean,
    cameraFacing: String,
    availableCameras: Array,
    selectedCamera: String
  })
  
  defineEmits([
    'update:selected-detector',
    'update:selected-recognizer',
    'update:selected-camera',
    'toggle-recognition',
    'toggle-camera',
    'update:show-face-box',
    'update:show-emotion-text',
    'update:show-emoji'
  ])
  </script>