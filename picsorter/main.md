# PicSorter

> An intelligent image organization tool that automatically identifies and sorts images containing people or flags.

[← Back to Project Collection](../README.md)

## Table of Contents
- [Origin](#origin)
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Technical Details](#technical-details)
- [Project Navigation](#project-navigation)

## Origin
Github Copilot and Claude 3.7 Sonnet prompted program.

**Original prompt:**
I want a script that moves any pictures that has people or flags in them to a new folder
***follow up Prompts:***
> I also want a logfile that includes the information on the weight and keywords


## Overview

This application uses computer vision and machine learning to:

1. Scan through a directory of images
2. Detect images containing people or flags
3. Move those images to a designated folder
4. Create detailed logs of the sorting process

## Features

- **Content Detection**: Uses MobileNetV2 pre-trained model to identify image content
- **Face Detection**: Supplements ML classification with OpenCV face detection
- **Detailed Logging**: Creates comprehensive logs with confidence scores and keywords
- **Batch Processing**: Processes multiple image formats at once
- **Command-line Interface**: Simple CLI with customizable source and destination
- **Robust Error Handling**: Continues processing even if individual images fail

## How It Works

1. **Model Loading**: Loads the MobileNetV2 pre-trained model
2. **Image Analysis**: For each image in the source directory:
   - Analyzes content using the model
   - Checks for people and flag-related keywords
   - Verifies face presence using OpenCV
3. **Sorting Logic**: Moves matching images to the destination directory
4. **Logging**: Records all activities, detections, and confidence scores

## Usage

### Basic Usage (Current Directory)

```powershell
python picsorter.py
```

This scans all images in the current directory and moves matching images to a "people_and_flags" subfolder.

### Specify Source Directory

```powershell
python picsorter.py C:\path\to\your\photos
```

### Specify Both Source and Destination Directories

```powershell
python picsorter.py C:\path\to\your\photos --dest C:\path\to\destination
```

## Requirements

- Python 3.6+
- TensorFlow
- OpenCV
- NumPy
- Pillow

## Installation

```powershell
pip install tensorflow opencv-python numpy pillow
```
### Note
The first time you run the script, it will download the MobileNetV2 model weights, which may take a moment depending on your internet connection.

## Log File Output

The application generates a detailed log file in the destination folder containing:

- Date and time of the sorting operation
- Source and destination directories
- For each detected image:
  - Keywords detected (e.g., "person", "flag")
  - Confidence scores for each detection
  - Whether detection was from ML model or face detection
- Summary statistics

## Customization

The application has several parameters that can be adjusted:

- **Confidence Threshold**: Minimum confidence score to count as a detection
- **Keywords**: Lists of people and flag-related keywords can be modified
- **Face Detection Parameters**: OpenCV face detection sensitivity can be tuned

## Libraries Used

This program utilizes the following open-source libraries:

### OpenCV (cv2)
OpenCV is an open-source library for computer vision and image processing. Here are some of its key capabilities:

- **Image Processing**:
  - Filters, transformations, and color space conversions
  - Histogram analysis and equalization
- **Video Analysis**:
  - Motion detection, background subtraction, and object tracking
- **Object Detection**:
  - Recognizes faces, eyes, cars, and more using pre-trained models
- **Camera Calibration and 3D Reconstruction**:
  - Calibrates cameras and reconstructs 3D models from images
- **Machine Learning**:
  - Includes tools for classification, regression, and clustering
- **Deep Learning Integration**:
  - Supports deep neural networks for advanced tasks
- **Image Stitching**:
  - Creates panoramas by stitching multiple images
- **Cross-Platform Support**:
  - Works on Windows, macOS, Linux, and mobile platforms

It's widely used in industries like healthcare, automotive, and robotics.

### TensorFlow and MediaPipe
The application uses TensorFlow for deep learning models like MobileNetV2, with capabilities similar to MediaPipe:

- **Computer Vision Tasks**:
  - Object detection and classification
  - Feature extraction from images
- **Pre-trained Models**:
  - Access to powerful pre-trained models like MobileNetV2
- **Cross-Platform Support**:
  - Works across various platforms and devices
- **Real-Time Processing**:
  - Optimized for efficient inference
- **Customization**:
  - Models can be fine-tuned for specific tasks
- **Efficiency**:
  - Models designed to work well even on devices with limited resources

These libraries enable the application to efficiently analyze images and identify specific content like people and flags.

---

## Project Navigation

- [← Back to Project Collection](../README.md)
- [Handstand Timer →](../handstandtimer/main.md)
- [High Kick Tracker →](../highkick/main.md)