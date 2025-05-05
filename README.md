## Projects Overview

### [Handstand Timer](handstandtimer/main.md)

A computer vision application that tracks handstands and times how long you can maintain the position. It uses MediaPipe hand tracking to detect when both hands are on the ground, automatically starting a timer and stopping it when hands leave the ground.

**Key Features:**
- Automatic handstand position detection
- Real-time timing and tracking
- Records and displays your best times
- Visual feedback with hand landmarks

[View Detailed Documentation](handstandtimer/main.md)

### [High Kick Tracker](highkick/main.md)

Measures and tracks how high you can kick using body pose estimation. The application establishes a baseline of your normal standing position, then calculates kick height as a percentage above this baseline.

**Key Features:**
- Automatic foot tracking and height measurement
- Baseline calibration from normal standing position
- Records your 10 highest kicks
- Visual feedback showing kick height

[View Detailed Documentation](highkick/main.md)

### [PicSorter](picsorter/main.md)

An intelligent image organization tool that automatically identifies and sorts images containing people or flags. It uses MobileNetV2 for image classification and OpenCV for supplementary face detection.

**Key Features:**
- Content-based image classification
- Detailed logging of detection results
- Command-line interface with flexible options
- Batch processing of multiple image formats

[View Detailed Documentation](picsorter/main.md)

## Technology Stack

All projects are built using Python and leverage the following key libraries:

- **OpenCV (cv2)**: For image processing, video capture, and basic object detection
- **MediaPipe**: For advanced hand tracking, pose estimation, and face detection
- **TensorFlow**: For deep learning models (PicSorter specifically)
- **NumPy**: For efficient numerical operations

## Origin

These projects were created with the assistance of AI tools:
- GitHub Copilot
- Claude 3.7 Sonnet

The implementation involved natural language prompts describing the desired functionality, followed by collaborative refinement to achieve the final applications.

---

*Created: May 5, 2025*