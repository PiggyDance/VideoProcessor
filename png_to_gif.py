from PIL import Image

def png_to_gif(png_file_path, gif_file_path):
    # 打开PNG文件
    png_image = Image.open(png_file_path)
    
    # 将PNG转换为GIF
    png_image.save(gif_file_path, 'GIF')


# 示例用法
png_to_gif(
    '/Volumes/disk/PiggyDance/SketchArtist/pen_shape/hand.png',
    '/Volumes/disk/PiggyDance/SketchArtist/pen_shape/hand.gif'
)
