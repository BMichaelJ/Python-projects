import cv2
import mediapipe as mp
import time

class HighKickTracker:
    def __init__(self):
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Kick tracking variables
        self.highest_kicks = []
        self.MAX_KICKS = 10
        self.exit_prompt_shown = False
        self.baseline_height = None
        self.baseline_frames = 0
        self.BASELINE_FRAMES_REQUIRED = 30
        self.kick_detected = False
        self.current_kick_height = 0
        self.kick_cooldown = 0
        self.KICK_COOLDOWN_FRAMES = 15
        
    def process_frame(self, frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape
        
        # Process the frame and detect body pose
        results = self.pose.process(rgb_frame)
        
        if results.pose_landmarks:
            # Draw pose landmarks
            self.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Get feet landmarks
            left_ankle = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
            left_foot_index = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
            right_foot_index = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
            
            # Calculate foot heights (lower y value means higher in the frame)
            left_foot_height = min(left_ankle.y, left_foot_index.y)
            right_foot_height = min(right_ankle.y, right_foot_index.y)
            
            # Get the height of the highest foot (in screen coordinates)
            current_highest_point = min(left_foot_height, right_foot_height)
            
            # Establish baseline height (ground level) in the first few frames
            if self.baseline_height is None or self.baseline_frames < self.BASELINE_FRAMES_REQUIRED:
                # During baseline detection, take the lowest foot position (highest y)
                if self.baseline_height is None:
                    self.baseline_height = max(left_foot_height, right_foot_height)
                else:
                    # Update baseline to be the lowest position seen
                    self.baseline_height = max(self.baseline_height, max(left_foot_height, right_foot_height))
                self.baseline_frames += 1
                
                # Draw baseline detection text
                baseline_text = f"Establishing baseline: {self.baseline_frames}/{self.BASELINE_FRAMES_REQUIRED}"
                cv2.putText(frame, baseline_text, (20, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            else:
                # Calculate kick height as a percentage of screen height
                # Baseline is 0%, top of screen would be 100%
                kick_height_percent = ((self.baseline_height - current_highest_point) / self.baseline_height) * 100
                
                # Handle kick detection and tracking
                if self.kick_cooldown > 0:
                    self.kick_cooldown -= 1
                
                # Detect if currently in a kick motion
                if kick_height_percent > 15:  # Threshold for kick detection
                    # Track the highest point of the current kick
                    if not self.kick_detected:
                        self.kick_detected = True
                        self.current_kick_height = kick_height_percent
                    else:
                        self.current_kick_height = max(self.current_kick_height, kick_height_percent)
                    
                    # Draw current kick height
                    kick_text = f"Current: {self.current_kick_height:.1f}%"
                    cv2.putText(frame, kick_text, (20, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif self.kick_detected and self.kick_cooldown == 0:
                    # End of kick detected
                    if self.current_kick_height > 15:  # Minimum threshold to count as a kick
                        self.highest_kicks.append(self.current_kick_height)
                        # Sort kicks in descending order and keep only the top MAX_KICKS
                        self.highest_kicks = sorted(self.highest_kicks, reverse=True)[:self.MAX_KICKS]
                    
                    self.kick_detected = False
                    self.current_kick_height = 0
                    self.kick_cooldown = self.KICK_COOLDOWN_FRAMES
            
            # Visualize the baseline
            baseline_y = int(self.baseline_height * h)
            cv2.line(frame, (0, baseline_y), (w, baseline_y), (0, 0, 255), 2)
            
            # Draw visual indicator of current foot height
            if self.baseline_height is not None:
                foot_y = int(current_highest_point * h)
                cv2.circle(frame, (w - 50, foot_y), 10, (0, 255, 0), -1)
                cv2.line(frame, (w - 50, baseline_y), (w - 50, foot_y), (0, 255, 0), 2)
        
        # Display kick history
        self.display_kick_history(frame)
        
        # Show exit prompt after MAX_KICKS
        if len(self.highest_kicks) >= self.MAX_KICKS and not self.exit_prompt_shown:
            self.display_exit_prompt(frame)
            self.exit_prompt_shown = True
        
        return frame
    
    def display_kick_history(self, frame):
        """Display list of highest kicks on right side of frame"""
        h, w, _ = frame.shape
        
        # Create a solid black background for the kick list
        if self.highest_kicks:
            # Calculate box dimensions
            box_height = 40 + len(self.highest_kicks) * 30  # Header + kicks
            box_width = 210
            
            # Draw solid black background
            cv2.rectangle(frame, (w - box_width - 10, 130), 
                         (w - 10, 140 + box_height), (0, 0, 0), -1)
            
            # Header for kicks list
            cv2.putText(frame, "Highest Kicks:", (w - 200, 160), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # List kicks
            for i, height in enumerate(self.highest_kicks):
                y_pos = 190 + i * 30
                kick_text = f"#{i+1}: {height:.1f}%"
                
                # Best kick in green, others in white
                text_color = (0, 255, 0) if i == 0 else (255, 255, 255)
                cv2.putText(frame, kick_text, (w - 200, y_pos), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
        
        # Display attempts counter
        kicks_left = self.MAX_KICKS - len(self.highest_kicks)
        if kicks_left > 0:
            attempts_text = f"Kicks left: {kicks_left}"
            cv2.putText(frame, attempts_text, (20, h - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    def display_exit_prompt(self, frame):
        """Display exit prompt after maximum kicks recorded"""
        h, w, _ = frame.shape
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (int(w/4), int(h/3)), (int(3*w/4), int(2*h/3)), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Display prompt text
        prompt_text1 = "10 highest kicks recorded!"
        prompt_text2 = "Press 'q' to exit"
        
        text_size1 = cv2.getTextSize(prompt_text1, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_size2 = cv2.getTextSize(prompt_text2, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        
        text_x1 = int((w - text_size1[0]) / 2)
        text_x2 = int((w - text_size2[0]) / 2)
        
        text_y1 = int(h/2 - 20)
        text_y2 = int(h/2 + 20)
        
        cv2.putText(frame, prompt_text1, (text_x1, text_y1), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, prompt_text2, (text_x2, text_y2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    def run(self):
        """Main method to run the high kick tracker"""
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        
        # Set fullscreen window
        cv2.namedWindow('High Kick Tracker', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('High Kick Tracker', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Process the frame
            processed_frame = self.process_frame(frame)
            
            # Display the frame
            cv2.imshow('High Kick Tracker', processed_frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        self.pose.close()

if __name__ == "__main__":
    print("Starting High Kick Tracker...")
    print("Please stand in your normal position for a few seconds to establish baseline.")
    print("The program will track your 10 highest kicks.")
    print("Press 'q' to quit.")
    
    tracker = HighKickTracker()
    tracker.run()