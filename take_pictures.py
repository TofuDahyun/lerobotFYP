import cv2
import os
import time
import msvcrt  # Windows-only, built-in module

# Configuration
BASE_DIR = "imagesegpics"
TARGET_WIDTH =  640
TARGET_HEIGHT = 480
SAVE_INTERVAL = 0.5  # seconds

def ensure_base_directory():
    """Creates the base directory if it doesn't exist."""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        print(f"Created base directory: {BASE_DIR}")

def get_existing_folders():
    """Scans the base directory and returns a list of subfolder names."""
    items = os.listdir(BASE_DIR)
    folders = [item for item in items if os.path.isdir(os.path.join(BASE_DIR, item))]
    return folders

def get_next_file_index(folder_path, folder_name):
    """
    Scans the folder to find the highest existing index 
    to continue numbering sequentially.
    """
    max_index = 0
    if not os.path.exists(folder_path):
        return 1
        
    files = os.listdir(folder_path)
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            name_part = os.path.splitext(file)[0]
            parts = name_part.split('_')
            
            if len(parts) >= 2:
                try:
                    index = int(parts[-1])
                    if index > max_index:
                        max_index = index
                except ValueError:
                    continue
    return max_index + 1

def select_folder():
    """Handles user interaction to select or create a folder."""
    ensure_base_directory()
    existing_folders = get_existing_folders()

    print("\n--- Folder Selection ---")
    if existing_folders:
        print("Existing folders in 'imagesegpics':")
        for i, folder in enumerate(existing_folders, 1):
            print(f"{i}. {folder}")
    else:
        print("No existing folders found in 'imagesegpics'.")

    print("\nType the name of an existing folder to use it,")
    print("or type a NEW name to create a new folder.")
    
    while True:
        choice = input("Enter folder name: ").strip()
        if not choice:
            print("Folder name cannot be empty.")
            continue
        
        folder_path = os.path.join(BASE_DIR, choice)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created new folder: {folder_path}")
        else:
            print(f"Using existing folder: {folder_path}")
            
        return choice, folder_path

def get_key():
    """Non-blocking keyboard input for Windows."""
    if msvcrt.kbhit():
        key = msvcrt.getch().decode('utf-8').lower()
        return key
    return None

def main():
    # 1. Folder Selection
    folder_name, folder_path = select_folder()
    
    # 2. Determine starting file index
    next_index = get_next_file_index(folder_path, folder_name)
    
    # 3. Camera Setup
    cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, TARGET_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, TARGET_HEIGHT)

    # 4. State Variables
    is_saving = False
    last_save_time = 0
    current_index = next_index

    print("\n--- Controls ---")
    print("Press 's' to Start/Resume saving")
    print("Press 'x' to Pause saving")
    print("Press 'q' to Quit")
    print("Make sure this terminal window has focus when pressing keys!")
    print("----------------\n")
    print("Camera started. Press 's' to begin capturing...\n")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))

            current_time = time.time()
            
            if is_saving:
                if current_time - last_save_time >= SAVE_INTERVAL:
                    filename = f"{folder_name}_{current_index}.jpg"
                    filepath = os.path.join(folder_path, filename)
                    
                    cv2.imwrite(filepath, frame)
                    print(f"Saved: {filename}")
                    
                    current_index += 1
                    last_save_time = current_time

            key = get_key()
            if key == 's':
                is_saving = True
                last_save_time = time.time()
                print(">> Saving Started")
            elif key == 'x':
                is_saving = False
                print(">> Saving Paused")
            elif key == 'q':
                print(">> Quitting Program")
                break

            time.sleep(0.01)  # Small delay to prevent CPU overload

    except KeyboardInterrupt:
        print("\n>> Interrupted by user")

    cap.release()
    print("Camera released. Program ended.")

if __name__ == "__main__":
    main()