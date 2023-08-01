import sys
import os
import json
import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from ultralytics import YOLO
import cv2


def inference(inputs : list):
  return_flags = list()

  basicImage = [inputs[0]]
  print(basicImage)
  yolo = inputs[1]
  print(yolo)
  tflite = inputs[2]
  print(tflite)

  seg_model = YOLO(yolo)

  unet = tf.lite.Interpreter(model_path=tflite)
  unet.allocate_tensors()
  input_details = unet.get_input_details()
  output_details = unet.get_output_details()
  input_shape = input_details[0]['shape']

  for input in basicImage:
    image = np.array(Image.open(input))
    # axs[0, 0].imshow(image)
    # axs[0, 0].set_title("Original Image")
    # axs[0, 0].axis('off')

    h, w, _ = image.shape
    results = seg_model.predict(input)

    for result in results:
      masks = result.masks
      boxes = result.boxes

    if masks is not None:
      for mask, box in zip(masks.data, boxes.data):
        mask = cv2.resize(np.array(mask.cpu()).astype(np.uint8), dsize=(w, h), interpolation=cv2.INTER_CUBIC)
        bbox = int(box[1]), int(box[3]), int(box[0]), int(box[2])
        mask = mask[bbox[0]:bbox[1], bbox[2]:bbox[3]]
        sliced_img = image[bbox[0]:bbox[1], bbox[2]:bbox[3]]

        sliced_img = cv2.resize(sliced_img, dsize=(128, 128), interpolation=cv2.INTER_CUBIC)
        sliced_img = np.array(sliced_img) / 255.0

        unet.set_tensor(input_details[0]['index'], sliced_img.reshape(1, 128, 128, 3).astype(np.float32))
        unet.invoke()

        output = unet.get_tensor(output_details[0]['index'])
        output = cv2.resize(output[0], dsize=(bbox[3]-bbox[2], bbox[1]-bbox[0]), interpolation=cv2.INTER_CUBIC)

        masked_img1 = mask * output[:, :, 0]
        masked_img2 = mask * output[:, :, 1]
        masked_img3 = mask * output[:, :, 2]
        output = cv2.merge((masked_img1, masked_img2, masked_img3))

        sliced_img = image[bbox[0]:bbox[1], bbox[2]:bbox[3]]

        mask = mask ^ True
        masked_img1 = mask * sliced_img[:, :, 0]
        masked_img2 = mask * sliced_img[:, :, 1]
        masked_img3 = mask * sliced_img[:, :, 2]
        masked_img = cv2.merge((masked_img1, masked_img2, masked_img3))


        output = np.add(masked_img.astype(np.uint8), (output * 255).astype(np.uint8)).astype(np.uint8)
        image[bbox[0]:bbox[1], bbox[2]:bbox[3]] = output

        from PIL import Image
        im = Image.fromarray(image)
        im.save(f"./{input}_mainpulated.jpeg")

      return_flags.append(1)

    else:
      return_flags.append(0)

  print(return_flags)

if __name__ == '__main__':
    print(os.getcwd())
    inference(list(sys.argv[1:]))