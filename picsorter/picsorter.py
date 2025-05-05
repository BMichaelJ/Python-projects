import os
import argparse
import shutil
import time
from pathlib import Path
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

class ImageSorter:
    def __init__(self, source_dir=None, destination_dir=None):
        """Initialize the image sorter with source and destination directories."""
        self.source_dir = Path(source_dir) if source_dir else None
        self.destination_dir = Path(destination_dir) if destination_dir else None
        
        # Load the pre-trained model
        print("Loading MobileNetV2 model...")
        self.model = MobileNetV2(weights='imagenet')
        
        # Keywords for people detection
        self.people_keywords = {'person', 'people', 'man', 'woman', 'child', 'boy', 'girl', 
                              'human', 'face', 'portrait', 'male', 'female'}
                              
        # Keywords for flag detection
        self.flag_keywords = {'flag', 'banner', 'ensign', 'pennant'}
        
        # Face detection using OpenCV
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Initialize log file
        self.log_file = None

    def contains_person_or_flag(self, img_path):
        """Check if the image contains a person or a flag."""
        # Load and preprocess the image for MobileNetV2
        try:
            # Use MobileNetV2 for classification
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            
            # Predict
            preds = self.model.predict(x)
            results = decode_predictions(preds, top=5)[0]
            
            # Variables to track detected keywords and scores for logging
            detected_keywords = []
            
            # Check predictions for people or flag keywords
            for _, label, score in results:
                if score > 0.1:  # Confidence threshold
                    if any(keyword in label for keyword in self.people_keywords):
                        detected_keywords.append(f"person:{label}:{score:.4f}")
                        print(f"Found person ({label}) in {img_path.name} with confidence {score:.2f}")
                        if self.log_file:
                            self.log_file.write(f"IMAGE: {img_path.name}, KEYWORD: {label}, TYPE: person, CONFIDENCE: {score:.4f}\n")
                        return True, detected_keywords
                    elif any(keyword in label for keyword in self.flag_keywords):
                        detected_keywords.append(f"flag:{label}:{score:.4f}")
                        print(f"Found flag ({label}) in {img_path.name} with confidence {score:.2f}")
                        if self.log_file:
                            self.log_file.write(f"IMAGE: {img_path.name}, KEYWORD: {label}, TYPE: flag, CONFIDENCE: {score:.4f}\n")
                        return True, detected_keywords
            
            # Additional check for faces using OpenCV
            img_cv2 = cv2.imread(str(img_path))
            if img_cv2 is not None:
                gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                if len(faces) > 0:
                    detected_keywords.append(f"face:opencv_detection:{len(faces)}")
                    print(f"Found {len(faces)} face(s) in {img_path.name}")
                    if self.log_file:
                        self.log_file.write(f"IMAGE: {img_path.name}, KEYWORD: face_detection, TYPE: person, FACES: {len(faces)}\n")
                    return True, detected_keywords
            
            return False, []
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            if self.log_file:
                self.log_file.write(f"ERROR: {img_path.name}, EXCEPTION: {str(e)}\n")
            return False, []

    def sort_images(self, source_dir=None, destination_dir=None):
        """Sort images from source directory to destination directory."""
        if source_dir:
            self.source_dir = Path(source_dir)
        if destination_dir:
            self.destination_dir = Path(destination_dir)
            
        # Validate directories
        if not self.source_dir or not self.source_dir.exists():
            raise ValueError(f"Source directory '{self.source_dir}' does not exist.")
            
        if not self.destination_dir:
            # Create a subdirectory "people_and_flags" in the source directory
            self.destination_dir = self.source_dir / "people_and_flags"
            
        # Create destination directory if it doesn't exist
        os.makedirs(self.destination_dir, exist_ok=True)
        
        # Create log file
        log_path = self.destination_dir / "picsorter_log.txt"
        self.log_file = open(log_path, 'w')
        self.log_file.write(f"PicSorter Log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log_file.write("=" * 80 + "\n")
        self.log_file.write(f"Source directory: {self.source_dir}\n")
        self.log_file.write(f"Destination directory: {self.destination_dir}\n")
        self.log_file.write("=" * 80 + "\n\n")
        self.log_file.write("IMAGE SORTING LOG (FORMAT: IMAGE, KEYWORD, TYPE, CONFIDENCE/DETAILS)\n\n")
        
        # Keep track of statistics
        stats = {"total": 0, "moved": 0, "errors": 0}
        
        # Get list of image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(list(self.source_dir.glob(f"*{ext}")))
            image_files.extend(list(self.source_dir.glob(f"*{ext.upper()}")))
            
        stats["total"] = len(image_files)
        print(f"Found {stats['total']} images in {self.source_dir}")
        self.log_file.write(f"Total images found: {stats['total']}\n\n")
        
        # Process each image
        for img_path in image_files:
            print(f"Processing {img_path.name}...")
            
            try:
                matched, keywords = self.contains_person_or_flag(img_path)
                if matched:
                    # Move the image to the destination directory
                    destination_path = self.destination_dir / img_path.name
                    shutil.move(str(img_path), str(destination_path))
                    stats["moved"] += 1
                    print(f"Moved {img_path.name} to {self.destination_dir}")
                    
                    # Add detailed log entry
                    self.log_file.write(f"MOVED: {img_path.name} -> {self.destination_dir}\n")
                    self.log_file.write(f"  Keywords detected: {', '.join(keywords)}\n\n")
                else:
                    self.log_file.write(f"SKIPPED: {img_path.name} (No people or flags detected)\n")
            except Exception as e:
                stats["errors"] += 1
                print(f"Error processing {img_path.name}: {e}")
                self.log_file.write(f"ERROR: {img_path.name}, {str(e)}\n")
        
        # Print summary
        summary = f"\nSorting complete: {stats['moved']} of {stats['total']} images moved to {self.destination_dir}"
        if stats["errors"] > 0:
            summary += f"\nEncountered {stats['errors']} errors during processing"
        
        print(summary)
        self.log_file.write("\n" + "=" * 80 + "\n")
        self.log_file.write(f"SUMMARY: {stats['moved']} of {stats['total']} images moved, {stats['errors']} errors\n")
        self.log_file.write("=" * 80 + "\n")
        
        # Close log file
        self.log_file.close()
        print(f"Log file created at: {log_path}")
        
        return stats


def main():
    """Main function to run the image sorter."""
    parser = argparse.ArgumentParser(description='Sort images containing people or flags.')
    parser.add_argument('source', nargs='?', help='Source directory containing images')
    parser.add_argument('--dest', '-d', help='Destination directory for sorted images')
    
    args = parser.parse_args()
    
    # Use current directory if no source provided
    source_dir = args.source if args.source else os.getcwd()
    destination_dir = args.dest
    
    print(f"Source directory: {source_dir}")
    print(f"Destination directory: {destination_dir or 'Will create people_and_flags subfolder'}")
    
    # Create and run the sorter
    sorter = ImageSorter(source_dir, destination_dir)
    sorter.sort_images()


if __name__ == "__main__":
    main()
