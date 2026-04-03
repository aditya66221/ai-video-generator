import os
from diffusers import StableDiffusionPipeline
# import torch
# from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
# Load model once
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
)
pipe = pipe.to("cpu")  # change to "cuda" if GPU available

def generate_images(prompt, num_images=10):
    image_paths = []
    os.makedirs("static/temp_images", exist_ok=True)

    for i in range(num_images):
        modified_prompt = prompt + f", variation {i}"
        image = pipe(modified_prompt).images[0]

        path = f"static/temp_images/img_{i}.png"
        image.save(path)
        image_paths.append(path)

    return image_paths


def create_video(image_paths, output_path="static/outputs/video.mp4"):
    clip = ImageSequenceClip(image_paths, fps=2)
    clip.write_videofile(output_path, codec="libx264")

    return output_path


def generate_video(prompt):
    images = generate_images(prompt)
    video = create_video(images)
    return video