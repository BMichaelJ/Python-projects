# High Kick Tracker

> A computer vision application that measures and tracks how high you can kick.

## Overview

This application uses your webcam and computer vision to automatically:

1. Detect your feet position using body pose estimation
2. Track when your foot is in the air during a kick
3. Record the highest point reached during each kick
4. Keep a list of your 10 highest kicks

## Features

- **Foot Position Detection**: Uses MediaPipe Pose to track foot position
- **Baseline Establishment**: Detects your normal standing position as a reference point
- **Automatic Measurement**: Calculates kick height as a percentage of your baseline
- **Performance Tracking**: Keeps track of your 10 highest kicks with visual display
- **Best Performance Highlight**: Shows your best kick in green
- **Fullscreen Display**: Clean, fullscreen interface for easy viewing during practice
- **Visual Feedback**: Shows real-time pose tracking and kick height indicator

## How It Works

1. **Body Detection**: MediaPipe Pose tracking identifies your ankle and foot positions
2. **Baseline Detection**: The app records your normal standing position during initialization
3. **Height Calculation**: Measures kick height as percentage above your baseline
4. **History Management**: Records up to 10 kicks before prompting to exit

## Usage

1. **Setup**: Position your camera so it can see your full body
2. **Calibration**: Stand normally for a few seconds to establish the baseline
3. **Performance**: Perform kicks while facing the camera
4. **Review**: View your kick heights on screen and try to achieve higher kicks
5. **Exit**: Press 'q' at any time to quit the application

## Requirements

- Python 3.10+ recommended
- OpenCV
- MediaPipe
- NumPy

## Installation

```powershell
pip install opencv-python mediapipe numpy
```

## Running the Application

```powershell
python highkick.py
```

## Customization

The application has several constants that can be adjusted to fit your needs:

- **Baseline Detection**: Number of frames used to establish baseline can be adjusted
- **Kick Threshold**: Minimum height required to count as a kick can be modified
- **Cooldown Period**: Time between kick detection to avoid multiple counts for one kick
- **MAX_KICKS**: Maximum number of kicks to track before prompting to exit (default 10)

## Tips for Best Results

- Ensure good lighting for reliable body detection
- Wear contrasting clothes for better pose detection
- Position the camera at an appropriate distance to capture your full body
- Perform kicks that are clearly visible to the camera

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

### MediaPipe
MediaPipe is a versatile open-source framework developed by Google for building machine learning pipelines, especially for processing multimedia data like video, audio, and text. Here are some of its key capabilities:

- **Computer Vision Tasks**:
  - Hand and pose tracking
  - Face detection and landmark recognition
  - Object detection and segmentation
  - Gesture recognition
- **Audio Processing**:
  - Audio classification and feature extraction
- **Text Processing**:
  - Text classification and embedding
- **Cross-Platform Support**:
  - Works on Android, iOS, web, and desktop platforms
  - Can even run on embedded systems like Raspberry Pi
- **Real-Time Processing**:
  - Designed for real-time applications, making it ideal for interactive systems
- **Customization**:
  - Offers tools like MediaPipe Model Maker to tailor models for specific needs
- **Efficiency**:
  - Optimized for performance, even on devices with limited resources

It's widely used in applications ranging from augmented reality to fitness tracking and beyond.
