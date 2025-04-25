import { emotionLabels, emotionColors } from './emotions'

// 在canvas上绘制人脸和表情
export function drawFacesOnCanvas(ctx, results, showFaceBox, showEmotionText, showEmoji) {
  // 绘制结果
  results.forEach(face => {
    const [emotionCode, x1, y1, x2, y2] = face
    
    if (showFaceBox) {
      // 绘制人脸框
      ctx.lineWidth = 3
      ctx.strokeStyle = emotionColors[emotionCode] || '#FFFFFF'
      ctx.strokeRect(x1, y1, x2 - x1, y2 - y1)
    }
    
    if (showEmotionText || showEmoji) {
      // 绘制表情标签
      ctx.font = '20px Arial'
      ctx.fillStyle = 'white'
      ctx.strokeStyle = 'black'
      ctx.lineWidth = 1
      
      let labelText = ''
      if (showEmotionText) {
        labelText += emotionLabels[emotionCode][0]
      }
      if (showEmoji) {
        if (labelText) labelText += ' '
        labelText += emotionLabels[emotionCode][1]
      }
      
      // 添加背景以提高可读性
      const textWidth = ctx.measureText(labelText).width
      ctx.fillStyle = 'rgba(0, 0, 0, 0.6)'
      ctx.fillRect(x1, y1 - 30, textWidth + 10, 30)
      
      // 绘制文本
      ctx.fillStyle = 'white'
      ctx.fillText(labelText, x1 + 5, y1 - 8)
    }
  })
}