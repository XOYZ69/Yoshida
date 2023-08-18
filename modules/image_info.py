from PIL import Image

import math

def img_get_color_avg(image_param:Image, mode = 'normal'):
    sum_pixel   = [0, 0, 0]
    divider_sum = 0

    cache_vector_w = (0 - (image_param.size[0] / 2)) ** 2
    cache_vector_h = (0 - (image_param.size[0] / 2)) ** 2
    max_distance_from_center = math.sqrt(cache_vector_w + cache_vector_h)

    for px_w in range(image_param.size[0]):
        for px_h in range(image_param.size[1]):
            match mode:
                case 'normal':
                    mulitplier = 1
                case 'center':
                    # d=√((x2 – x1)² + (y2 – y1)²)
                    cache_vector_w = (px_w - (image_param.size[0] / 2)) ** 2
                    cache_vector_h = (px_h - (image_param.size[0] / 2)) ** 2
                    mulitplier = math.sqrt(cache_vector_w + cache_vector_h)
                case other:
                    mulitplier = 1

            current_pixel = image_param.getpixel((px_w, px_h))
            sum_pixel = [
                sum_pixel[0] + (current_pixel[0] * mulitplier),
                sum_pixel[1] + (current_pixel[1] * mulitplier),
                sum_pixel[2] + (current_pixel[2] * mulitplier),
            ]
            divider_sum += mulitplier
    
    sum_pixel = [
        int(sum_pixel[0] / divider_sum),
        int(sum_pixel[1] / divider_sum),
        int(sum_pixel[2] / divider_sum)
    ]

    return sum_pixel
