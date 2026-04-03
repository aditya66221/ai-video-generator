import os
from diffusers import StableDiffusionPipeline
import torch
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

# Load model once
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
)

# Use CPU (or GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)


def generate_images(prompt, num_images=5):  # reduced from 10 → 5
    image_paths = []

    os.makedirs("static/temp_images", exist_ok=True)

    for i in range(num_images):
        modified_prompt = prompt + f", variation {i}"

        image = pipe(
            modified_prompt,
            num_inference_steps=20  # reduced steps (FAST)
        ).images[0]

        path = f"static/temp_images/img_{i}.png"
        image.save(path)
        image_paths.append(path)

    return image_paths


def create_video(image_paths, output_path="static/outputs/video.mp4"):
    os.makedirs("static/outputs", exist_ok=True)

    clip = ImageSequenceClip(image_paths, fps=2)
    clip.write_videofile(output_path, codec="libx264")

    return output_path


def generate_video(prompt):
    images = generate_images(prompt)
    video = create_video(images)
    return video