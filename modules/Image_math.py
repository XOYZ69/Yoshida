def get_alpha_calculation(pixel_a, pixel_b):
    luma = pixel_a[3] + pixel_b[3]

    luma_color = (
        ((pixel_a[0] * pixel_a[3]) + (pixel_b[0] * pixel_b[3])) // luma,
        ((pixel_a[1] * pixel_a[3]) + (pixel_b[1] * pixel_b[3])) // luma,
        ((pixel_a[2] * pixel_a[3]) + (pixel_b[2] * pixel_b[3])) // luma,
        255
    )

    return luma_color

def get_alpha_v2_calculation(pixel_a, pixel_b):

    luma_color = (
        int((pixel_a[0] * pixel_a[3] / 255) + (pixel_b[0] * pixel_b[3] * (255 - pixel_a[3] / (255 * 255)))),
        int((pixel_a[1] * pixel_a[3] / 255) + (pixel_b[1] * pixel_b[3] * (255 - pixel_a[3] / (255 * 255)))),
        int((pixel_a[2] * pixel_a[3] / 255) + (pixel_b[2] * pixel_b[3] * (255 - pixel_a[3] / (255 * 255)))),
        255
    )

    return luma_color

def get_alpha_v2_reverse_calculation(pixel_a, pixel_b):
    
    weight_a = min(0, 255 - (pixel_a[3] - pixel_b[3]))
    weight_b = 255 - weight_a

    luma_color = (
        ((pixel_a[0] * weight_a) + (pixel_b[0] * weight_b)) // (255),
        ((pixel_a[1] * weight_a) + (pixel_b[1] * weight_b)) // (255),
        ((pixel_a[2] * weight_a) + (pixel_b[2] * weight_b)) // (255),
        pixel_a[3],
    )

    return luma_color

def get_brightness(pixel):
    return (pixel[0] + pixel[1] + pixel[2]) // 3
