import PIL
import numpy as np
import cv2

def save_image(output_images, count, src_number, dest_number):
    if count == 1:
        ref = PIL.Image.open(f'resized-new/reference1.jpg')
        _, h = ref.size
        img = PIL.Image.open(output_images[0])
        img = np.array(img)
        width = 600
        ref = ref.resize((width, h))
        ref = np.array(ref)
        im_final = cv2.vconcat([img, ref])
        im_final = cv2.cvtColor(im_final, cv2.COLOR_BGR2RGB)
        cv2.imwrite(f'final-output-images/{src_number}-{dest_number}.jpg', im_final)
    elif count == 2:
        ref = PIL.Image.open(f'resized-new/reference2.jpg')
        im1 = cv2.imread(output_images[0])
        im2 = cv2.imread(output_images[1])
        im_h = cv2.hconcat([im1, im2])
        ref = np.array(ref)
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2RGB)
        im_final = cv2.vconcat([im_h, ref])
        cv2.imwrite(f'final-output-images/{src_number}-{dest_number}.jpg', im_final)
    elif count == 3:
        ref = PIL.Image.open(f'resized-new/reference3.jpg')
        if '-2-1-' in output_images[1] and '-3-0-' in output_images[2]:
            im1 = cv2.imread(output_images[1])
            im2 = cv2.imread(output_images[0])
            im3 = cv2.imread(output_images[2])
        else:
            im1 = cv2.imread(output_images[0])
            im2 = cv2.imread(output_images[1])
            im3 = cv2.imread(output_images[2])
        im_h = cv2.hconcat([im1, im2, im3])
        ref = np.array(ref)
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2RGB)
        im_final = cv2.vconcat([im_h, ref])
        cv2.imwrite(f'final-output-images/{src_number}-{dest_number}.jpg', im_final)
    elif count == 4:
        ref = PIL.Image.open(f'resized-new/reference4.jpg')
        if ('-2-1-' in output_images[1] and '-3-0-' in output_images[2]):
            im1 = cv2.imread(output_images[1])
            im2 = cv2.imread(output_images[0])
            im3 = cv2.imread(output_images[2])
            im4 = cv2.imread(output_images[3])
        else:
            im1 = cv2.imread(output_images[0])
            im2 = cv2.imread(output_images[1])
            im3 = cv2.imread(output_images[2])
            im4 = cv2.imread(output_images[3])
        im_final = cv2.hconcat([im1, im2, im3, im4])
        ref = np.array(ref)
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2RGB)
        im_final = cv2.vconcat([im_final, ref])
        # im_final = cv2.resize(im_final, (960,480))
        cv2.imwrite(f'final-output-images/{src_number}-{dest_number}.jpg', im_final)