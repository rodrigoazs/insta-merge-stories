import os

from PIL import Image


def get_images_from_folder(folder_path, extensions=None):
    """
    Get a list of image file paths from a folder.

    :param folder_path: Path to the folder containing images.
    :param extensions: A tuple of allowed image file extensions (default: common image formats).
    :return: A list of file paths for images in the folder.
    """
    if extensions is None:
        extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")  # Common image formats

    # List all files in the folder and filter by extensions
    images = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.lower().endswith(extensions)
    ]

    return sorted(images)


def format_three_16x9(image_paths, output_path):
    """
    Resize 3 images to width 2584px, create a white background of 2584px x 4603px,
    and place the images vertically with the first image at the top,
    the second centered, and the third at the bottom.

    This function expects three 16x9 pictures.

    :param image_paths: List of file paths for the three images.
    :param output_path: File path for the output image.
    """
    if len(image_paths) != 3:
        raise ValueError("Exactly three image paths are required.")

    # Define background dimensions
    bg_width = 2584
    bg_height = 4603
    background = Image.new("RGB", (bg_width, bg_height), "white")

    # Open images and resize them to width 2584px
    images = []
    for image_path in image_paths:
        img = Image.open(image_path)
        aspect_ratio = img.height / img.width
        new_width = bg_width
        new_height = int(new_width * aspect_ratio)
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        images.append(resized_img)

    # Calculate placement positions
    top_image = images[0]
    bottom_image = images[2]
    center_image = images[1]

    # Calculate y-coordinates
    y_top = 0
    y_center = (bg_height - center_image.height) // 2
    y_bottom = bg_height - bottom_image.height

    # Place the images on the background
    background.paste(top_image, (0, y_top))
    background.paste(center_image, (0, y_center))
    background.paste(bottom_image, (0, y_bottom))

    # Save the final image
    background.save(output_path, format="JPEG", quality=100)
    print(f"Final image saved at: {output_path}")


def main():
    image_paths = get_images_from_folder("three_16x9")
    if len(image_paths) % 3:
        raise ValueError("Exactly a multiple of three image paths is required.")
    for i in range(0, len(image_paths), 3):
        format_three_16x9(image_paths[i : i + 3], f"output{i}.jpg")


main()
