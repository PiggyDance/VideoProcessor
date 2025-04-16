from pixelate_and_remove_bg import remove_background
from pathlib import Path

path = '/Volumes/disk/tmp/flowerpngs/live_multilink_stage_flower_petal4_6.png'

rm_bg_image = remove_background(path)
input_path = Path(path)
output_path = input_path.with_stem(f"{input_path.stem}_remove_bg")

# 保存像素化后的图片
rm_bg_image.save(output_path, "PNG")
