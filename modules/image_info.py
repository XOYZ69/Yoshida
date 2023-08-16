from PIL import Image

def img_get_color_avg(image_param):
    sum_pixel = [0, 0, 0]

    for px_w in range(image_param.size[0]):
        for px_h in range(image_param.size[1]):
            current_pixel = image_param.getpixel(px_w, px_h)
            sum_pixel = [
                sum_pixel[0] + current_pixel[0],
                sum_pixel[1] + current_pixel[1],
                sum_pixel[2] + current_pixel[2],
            ]

    pixel_sum = image_param.size[0] * image_param.size[1]

    sum_pixel = [
        sum_pixel[0] / pixel_sum,
        sum_pixel[1] / pixel_sum,
        sum_pixel[2] / pixel_sum
    ]
