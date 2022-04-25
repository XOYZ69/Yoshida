def get_alpha_calculation(pixel_a, pixel_b):
    luma = pixel_a[3] + pixel_b[3]

    luma_color = (
        ((pixel_a[0] * pixel_a[3]) + (pixel_b[0] * pixel_b[3])) // luma,
        ((pixel_a[1] * pixel_a[3]) + (pixel_b[1] * pixel_b[3])) // luma,
        ((pixel_a[2] * pixel_a[3]) + (pixel_b[2] * pixel_b[3])) // luma,
        255
    )

    return luma_color
