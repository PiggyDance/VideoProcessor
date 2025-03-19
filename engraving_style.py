"""
版画风格转换工具
使用示例：
python engraving_style.py --input portrait.jpg --output engraving.png --edge_threshold 50 --colors 4
"""

from PIL import Image
import cv2
import numpy as np
import argparse

def apply_engraving_effect(input_path, output_path, edge_threshold=50, color_levels=4, texture_path=None):
    # 读取并转换图像模式
    img = Image.open(input_path).convert('RGB')
    np_img = np.array(img)
    
    # 边缘检测
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, edge_threshold, edge_threshold*3)
    
    # 颜色量化
    quantized = np_img // (256//color_levels) * (256//color_levels)
    
    # 合成边缘与量化颜色
    edges_expanded = np.expand_dims(edges, axis=2)
    final = np.where(edges_expanded > 0, 0, quantized)
    
    # 转换为PIL图像并保存
        # 纹理叠加处理
    if args.texture:
        texture = Image.open(args.texture).convert('L')
    else:
        # 使用内置默认纹理
        texture = Image.open(Path(__file__).parent/'image'/'cartoon1.jpg').convert('L')
    
    # 调整纹理尺寸
    texture = texture.resize(final.shape[:2][::-1])
    np_texture = np.array(texture).astype(float)/255.0
    
    # 应用纹理（正片叠底混合）
    final = (final * np.expand_dims(np_texture, axis=2)).astype('uint8')
    
    Image.fromarray(final).save(output_path)
    print(f"版画风格图片已保存到：{output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='将写实人像转换为版画风格')
    parser.add_argument('--input', required=True, help='输入图片路径')
    parser.add_argument('--output', required=True, help='输出图片路径')
    parser.add_argument('--edge_threshold', type=int, default=50, help='边缘检测阈值（默认50）')
    parser.add_argument('--colors', type=int, default=4, help='颜色层级（默认4）')
    parser.add_argument('--texture', help='纹理图片路径（默认使用内置纹理）')
    
    args = parser.parse_args()
    
    apply_engraving_effect(
        args.input,
        args.output,
        edge_threshold=args.edge_threshold,
        color_levels=args.colors
    )