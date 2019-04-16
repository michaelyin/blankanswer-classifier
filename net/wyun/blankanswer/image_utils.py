import PIL
from PIL import Image
import numpy as np

def crop_image(img, output_path, default_size=None):
    old_im = Image.open(img).convert('L')
    img_data = np.asarray(old_im, dtype=np.uint8) # height, width
    nnz_inds = np.where(img_data!=255)
    if len(nnz_inds[0]) == 0:
        if not default_size:
            old_im.save(output_path)
            return None
        else:
            assert len(default_size) == 2, default_size
            x_min,y_min,x_max,y_max = 0,0,default_size[0],default_size[1]
            old_im = old_im.crop((x_min, y_min, x_max+1, y_max+1))
            old_im.save(output_path)
            return None
    y_min = np.min(nnz_inds[0])
    y_max = np.max(nnz_inds[0])
    x_min = np.min(nnz_inds[1])
    x_max = np.max(nnz_inds[1])
    old_im = old_im.crop((x_min, y_min, x_max+1, y_max+1))
    #old_im.save(output_path)
    return old_im


def pad_image(old_im, output_path, pad_size, buckets):
    #PAD_TOP, PAD_LEFT, PAD_BOTTOM, PAD_RIGHT = pad_size
    PAD_TOP, PAD_LEFT, PAD_BOTTOM, PAD_RIGHT = (8, 8,8,8)
    old_size = (old_im.size[0]+PAD_LEFT+PAD_RIGHT, old_im.size[1]+PAD_TOP+PAD_BOTTOM)
    new_size = old_size
    new_im = Image.new("RGB", new_size, (255,255,255))
    new_im.paste(old_im, (PAD_LEFT,PAD_TOP))
    #new_im.save(output_path)
    return new_im

def downsample_image(old_im, output_path, ratio):
    assert ratio>=1, ratio
    if ratio == 1:
        return True
    old_size = old_im.size
    new_size = (int(old_size[0]/ratio), int(old_size[1]/ratio))

    new_im = old_im.resize(new_size, PIL.Image.LANCZOS)
    new_im.save(output_path)
    return True
