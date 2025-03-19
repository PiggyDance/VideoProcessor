from pixelate_and_remove_bg import remove_background
from pathlib import Path

path = '/Volumes/disk/LynxProjects/webcast_hybrid-social/apps/linkmic_dynamic_lynx/src/images/live_multilink_staeg_flower_petal2.jpg'

rm_bg_image = remove_background(path)
input_path = Path(path)
output_path = input_path.with_stem(f"{input_path.stem}_remove_bg")

# 保存像素化后的图片
rm_bg_image.save(output_path, "PNG")
