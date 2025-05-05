

# Handstand Timer

> A computer vision application that tracks handstands and times how long you can maintain the position.

## Origin
Github Copilot and Claude 3.7 Sonnet prompted program.
Idea came from timing my daughters handstands and wanted to "gamify" the training for her.

**Original Prompt:**
> I am writing a python program that will take time how long one can stand on their hands. The idea is to use camera to detect when both hands touch the floor and start timer until both hands release the floor. Can you help me write this code?

## Overview

This application uses your webcam and computer vision to automatically:

1. Detect when both hands are on the ground in a handstand position
2. Time how long you maintain the handstand position
3. Track and display your best times
4. Store a history of your attempts

## Features

- **Hand Position Detection**: Uses MediaPipe hand tracking to identify when hands are properly positioned on the ground
- **Automatic Timing**: Starts automatically when a handstand is detected and stops when the position is released
- **Performance Tracking**: Keeps track of up to 10 attempts with visual display of all times
- **Best Performance Highlight**: Shows your best time in green
- **Fullscreen Display**: Clean, fullscreen interface for easy viewing during exercise
- **Visual Feedback**: Shows real-time hand tracking with landmarks and connections

## How It Works

1. **Hand Detection**: MediaPipe's hand tracking identifies the position of your wrists and fingers
2. **Position Analysis**: The app checks if the wrist is above the fingertips and if fingertips are near the bottom of the frame
3. **Timing Logic**: Timing starts after a brief stabilization period and stops when hands leave the ground
4. **History Management**: Records up to 10 attempts before prompting to exit

## Usage

1. **Setup**: Position your camera so it can see the floor area where you'll perform handstands
2. **Start**: Run the application and stand in view of the camera
3. **Perform**: Get into a handstand position with both hands on the ground
4. **Review**: View your times on screen and try to beat your best time
5. **Exit**: Press 'q' at any time to quit the application

## Requirements

- Python 3.10+ recommended
- OpenCV
- MediaPipe
- NumPy

## Installation

```bash
pip install opencv-python mediapipe numpy
```

## Running the Application

```bash
python handstandtimer.py
```

## Customization

The application has several constants that can be adjusted to fit your needs:

- `GROUND_THRESHOLD_RATIO`: Controls how high in the frame hands need to be to count as "on ground"
- `STABLE_FRAMES_REQUIRED`: Number of frames the hands must be in position before timing starts
- `MIN_HANDS_FOR_HANDSTAND`: Number of hands required to be detected (default 2)
- `MAX_ATTEMPTS`: Maximum number of attempts to track before prompting to exit (default 10)

## Tips for Best Results

- Ensure good lighting for reliable hand detection
- Position the camera at an appropriate height and angle
- Wear contrasting colors to the floor for better detection
- Allow a few seconds of stabilization before starting your handstand

## Related Projects

- **HighKick Tracker**: Similar application for measuring kick height
- **PicSorter**: Utility for sorting images based on content detection

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