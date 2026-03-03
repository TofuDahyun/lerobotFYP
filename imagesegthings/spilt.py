import os
import shutil
import random

def split_dataset(root_dir, split_ratio=0.2, seed=42):
    # Define paths relative to the root directory
    img_train_dir = os.path.join(root_dir, 'images', 'train')
    img_val_dir = os.path.join(root_dir, 'images', 'val')
    lbl_train_dir = os.path.join(root_dir, 'labels', 'train')
    lbl_val_dir = os.path.join(root_dir, 'labels', 'val')

    # Create validation directories if they don't exist
    os.makedirs(img_val_dir, exist_ok=True)
    os.makedirs(lbl_val_dir, exist_ok=True)

    # Get list of all files in image training directory
    # We filter to ensure we only pick image files (jpg, png, etc)
    all_files = os.listdir(img_train_dir)
    image_files = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

    total_images = len(image_files)
    if total_images == 0:
        print("No images found in images/train!")
        return

    # Calculate split count
    val_count = int(total_images * split_ratio)
    
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Randomly select files for validation
    val_files = random.sample(image_files, val_count)

    print(f"Total images found: {total_images}")
    print(f"Moving {val_count} images ({split_ratio*100}%) to validation set...")

    moved_count = 0

    for filename in val_files:
        # --- Handle Images ---
        src_img_path = os.path.join(img_train_dir, filename)
        dst_img_path = os.path.join(img_val_dir, filename)

        # --- Handle Labels ---
        # Change extension from .jpg (or similar) to .txt
        name_without_ext = os.path.splitext(filename)[0]
        label_filename = f"{name_without_ext}.txt"
        
        src_lbl_path = os.path.join(lbl_train_dir, label_filename)
        dst_lbl_path = os.path.join(lbl_val_dir, label_filename)

        # Move Image
        if os.path.exists(src_img_path):
            shutil.move(src_img_path, dst_img_path)
        else:
            print(f"Warning: Image not found {src_img_path}")

        # Move Label (if it exists)
        if os.path.exists(src_lbl_path):
            shutil.move(src_lbl_path, dst_lbl_path)
        else:
            # Sometimes images don't have labels, or naming differs slightly
            print(f"Warning: Corresponding label not found for {filename}, skipping label move.")

        moved_count += 1

    print(f"Successfully moved {moved_count} image/label pairs to validation set.")
    print(f"Remaining in train: {total_images - moved_count}")

if __name__ == "__main__":
    # Get the directory where the script is located (assumed to be root)
    root_directory = os.path.dirname(os.path.abspath(__file__))
    split_dataset(root_directory)