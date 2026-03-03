# test.py - FIXED VERSION for Windows
from ultralytics import YOLO
import os

def train_model():
    # Set working directory to where data.yaml is located
    os.chdir(r"C:\School Stuff\Year 4 Sem 2\FYP\lerobotFYP\imagesegthings")
    
    # Load pretrained segmentation model
    model = YOLO("yolov8n-seg.pt")
    
    # Train the model
    results = model.train(
        data="data.yaml",
        epochs=500,              # Keep low for testing
        imgsz=640,              # Your current size
        batch=4,                # Good for 4GB VRAM
        device=0,               # RTX 3050 Laptop GPU
        workers=0,              # ⚠️ CRITICAL: Set to 0 on Windows to avoid multiprocessing issues
        #project="runs/segment",
        name="actual_segmentation_500epochs",
        #patience=20,
        #save=True,
        #exist_ok=True,
        #cache=True,             # Cache labels for faster loading
        #close_mosaic=5          # Disable mosaic augmentation in last 5 epochs
    )
    
    print("✅ Training complete!")
    return results

# 🔥 THIS IS THE KEY FIX FOR WINDOWS 🔥
if __name__ == '__main__':
    # Optional: add freeze_support() if you plan to freeze to .exe later
    # from multiprocessing import freeze_support
    # freeze_support()
    
    train_model()