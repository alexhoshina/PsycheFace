import { emotionLabels, emotionColors } from './emotions'

// 在canvas上绘制人脸和表情
export function drawFacesOnCanvas(ctx, results, showFaceBox, showEmotionText, showEmoji) {
  // 获取canvas的实际尺寸
  const canvasWidth = ctx.canvas.width
  const canvasHeight = ctx.canvas.height
  
  console.log('绘制时的Canvas尺寸:', {
    width: canvasWidth,
    height: canvasHeight
  })
  
  // 绘制结果
  results.forEach(face => {
    const [emotionCode, x1, y1, x2, y2] = face
    
    console.log('原始坐标:', { x1, y1, x2, y2 })
    
    // 计算实际绘制坐标
    const drawX1 = Math.round(x1)
    const drawY1 = Math.round(y1)
    const drawX2 = Math.round(x2)
    const drawY2 = Math.round(y2)
    
    console.log('计算后的绘制坐标:', { drawX1, drawY1, drawX2, drawY2 })
    
    if (showFaceBox) {
      // 绘制人脸框
      ctx.lineWidth = 3
      ctx.strokeStyle = emotionColors[emotionCode] || '#FFFFFF'
      ctx.strokeRect(drawX1, drawY1, drawX2 - drawX1, drawY2 - drawY1)
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
      ctx.fillRect(drawX1, drawY1 - 30, textWidth + 10, 30)
      
      // 绘制文本
      ctx.fillStyle = 'white'
      ctx.fillText(labelText, drawX1 + 5, drawY1 - 8)
    }
  })
}