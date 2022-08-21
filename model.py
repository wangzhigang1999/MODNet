import cv2
import numpy as np
import onnxruntime
import uuid
from oss_util import upload

model_path = "modnet.onnx"

session = onnxruntime.InferenceSession(model_path, None)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

ref_size = 512
# TODO 补全这个前缀
oss_prefix = ""


# Get x_scale_factor & y_scale_factor to resize image
def get_scale_factor(im_h, im_w, ref_size):
    if max(im_h, im_w) < ref_size or min(im_h, im_w) > ref_size:
        if im_w >= im_h:
            im_rh = ref_size
            im_rw = int(im_w / im_h * ref_size)
        elif im_w < im_h:
            im_rw = ref_size
            im_rh = int(im_h / im_w * ref_size)
    else:
        im_rh = im_h
        im_rw = im_w

    im_rw = im_rw - im_rw % 32
    im_rh = im_rh - im_rh % 32

    x_scale_factor = im_rw / im_w
    y_scale_factor = im_rh / im_h

    return x_scale_factor, y_scale_factor


def inference(img_path, output_path):
    # read image
    im = cv2.imread(img_path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    # unify image channels to 3
    if len(im.shape) == 2:
        im = im[:, :, None]
    if im.shape[2] == 1:
        im = np.repeat(im, 3, axis=2)
    elif im.shape[2] == 4:
        im = im[:, :, 0:3]

    # normalize values to scale it between -1 to 1
    im = (im - 127.5) / 127.5

    im_h, im_w, im_c = im.shape
    x, y = get_scale_factor(im_h, im_w, ref_size)

    # resize image
    im = cv2.resize(im, None, fx=x, fy=y, interpolation=cv2.INTER_AREA)

    # prepare input shape
    im = np.transpose(im)
    im = np.swapaxes(im, 1, 2)
    im = np.expand_dims(im, axis=0).astype('float32')

    result = session.run([output_name], {input_name: im})

    # refine mask
    mask = (np.squeeze(result[0]) * 255).astype('uint8')
    mask = cv2.resize(mask, dsize=(im_w, im_h), interpolation=cv2.INTER_AREA)

    # mask = np.expand_dims(mask,-1)

    transparent = cv2.imread(img_path)

    # resout = np.where(mask!=0,transparent,0)

    r, g, b = cv2.split(transparent)
    img_rgba = cv2.merge((r, g, b, mask))

    cv2.imwrite(output_path, img_rgba)

    oss_name = "{}.png".format(uuid.uuid4())
    res = upload(oss_name, output_path)
    if res:
        return "{}/{}".format(oss_prefix, oss_name)
    return None


if __name__ == '__main__':
    inference("test.png", "test-o.png")
