/**
 * 表情识别系统API服务
 */

// API基础URL，可根据环境配置
const BASE_URL = '127.0.0.1:8000'; // 开发环境URL，空字符串表示相对路径

/**
 * 获取可用的模型列表
 * @returns {Promise<{detectorModels: string[], recognizerModels: string[]}>}
 */
export async function fetchModels() {
  try {
    const response = await fetch(`http://${BASE_URL}/models`);
    
    if (!response.ok) {
      throw new Error(`服务器错误: ${response.status}`);
    }
    
    const data = await response.json();
    
    // 验证响应数据格式
    if (!Array.isArray(data) || data.length !== 2) {
      throw new Error('模型数据格式不正确');
    }
    
    return {
      detectorModels: data[0] || [],
      recognizerModels: data[1] || []
    };
  } catch (error) {
    console.error('获取模型失败:', error);
    throw new Error(`获取模型列表失败: ${error.message}`);
  }
}

/**
 * 创建WebSocket连接
 * @param {string} detector - 人脸检测模型名称
 * @param {string} recognizer - 表情识别模型名称
 * @param {Object} callbacks - 回调函数对象
 * @param {Function} callbacks.onOpen - 连接成功回调
 * @param {Function} callbacks.onMessage - 收到消息回调
 * @param {Function} callbacks.onError - 错误回调
 * @param {Function} callbacks.onClose - 连接关闭回调
 * @returns {WebSocket} - WebSocket实例
 */
export function createWebSocketConnection(detector, recognizer, callbacks = {}) {
  const { onOpen, onMessage, onError, onClose } = callbacks;
  
  if (!detector || !recognizer) {
    throw new Error('必须提供检测器和识别器模型名称');
  }
  
  const wsUrl = `ws://${BASE_URL}/ws?detector=${detector}&recognizer=${recognizer}`;
  
  const socket = new WebSocket(wsUrl);
  
  if (onOpen) socket.onopen = onOpen;
  if (onMessage) socket.onmessage = event => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (error) {
      console.error('解析WebSocket响应失败:', error);
      if (onError) onError(new Error('解析服务器消息失败'));
    }
  };
  if (onError) socket.onerror = onError;
  if (onClose) socket.onclose = onClose;
  
  return socket;
}

/**
 * 通过WebSocket发送图像数据
 * @param {WebSocket} socket - WebSocket连接
 * @param {Blob|ArrayBuffer} imageData - 图像数据
 * @returns {Promise<boolean>} - 发送是否成功
 */
export async function sendImageData(socket, imageData) {
  return new Promise((resolve, reject) => {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      reject(new Error('WebSocket未连接'));
      return;
    }
    
    try {
      // 如果已经是ArrayBuffer，直接发送
      if (imageData instanceof ArrayBuffer) {
        socket.send(imageData);
        resolve(true);
        return;
      }
      
      // 如果是Blob，转换为ArrayBuffer
      if (imageData instanceof Blob) {
        const reader = new FileReader();
        reader.onload = () => {
          try {
            socket.send(reader.result);
            resolve(true);
          } catch (e) {
            reject(new Error(`发送图像数据失败: ${e.message}`));
          }
        };
        reader.onerror = () => reject(new Error('读取图像数据失败'));
        reader.readAsArrayBuffer(imageData);
        return;
      }
      
      // 如果是Canvas，转换为Blob然后发送
      if (imageData instanceof HTMLCanvasElement) {
        imageData.toBlob(blob => {
          const reader = new FileReader();
          reader.onload = () => {
            try {
              socket.send(reader.result);
              resolve(true);
            } catch (e) {
              reject(new Error(`发送图像数据失败: ${e.message}`));
            }
          };
          reader.onerror = () => reject(new Error('读取Canvas数据失败'));
          reader.readAsArrayBuffer(blob);
        }, 'image/jpeg', 0.8);
        return;
      }
      
      reject(new Error('不支持的图像数据类型'));
    } catch (error) {
      reject(new Error(`发送图像数据失败: ${error.message}`));
    }
  });
}


/**
 * 上传图像进行表情识别
 * @param {File} file - 要上传的图像文件
 * @param {string} detectorName - 人脸检测模型名称
 * @param {string} recognizerName - 情感识别模型名称
 * @returns {Promise<Array>} - 识别结果
 */
export async function uploadImageForPrediction(file, detectorName, recognizerName) {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const url = `http://${BASE_URL}/predict?detector_name=${encodeURIComponent(detectorName)}&recognizer_name=${encodeURIComponent(recognizerName)}`;
    
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`服务器错误 (${response.status}): ${errorText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('图像识别失败:', error);
    throw new Error(`图像识别请求失败: ${error.message}`);
  }
}