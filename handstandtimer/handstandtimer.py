import cv2
import mediapipe as mp
import time

class HandstandTimer:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Timer variables
        self.start_time = None
        self.end_time = None
        self.is_timing = False
        self.timer_history = []
        self.MAX_ATTEMPTS = 10
        self.exit_prompt_shown = False
        
        # Constants for hand position detection
        self.GROUND_THRESHOLD_RATIO = 0.85  # Lower threshold means higher up in the frame (since 0,0 is top-left)
        self.MIN_HANDS_FOR_HANDSTAND = 2
        self.STABLE_FRAMES_REQUIRED = 5
        self.stable_frame_counter = 0
        
    def hands_on_ground(self, hand_landmarks, frame_height):
        """Check if the hand appears to be on the ground (bottom of frame)"""
        # Check if wrist and fingers are near the bottom of the frame
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        
        # Check if the hand is positioned correctly (wrist higher than fingertips)
        if wrist.y < index_tip.y and wrist.y < middle_tip.y:
            # Check if the fingertips are near the bottom of the frame
            if (index_tip.y > self.GROUND_THRESHOLD_RATIO or 
                middle_tip.y > self.GROUND_THRESHOLD_RATIO):
                return True
        
        return False
    
    def process_frame(self, frame):
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape
        
        # Process the frame and detect hands
        results = self.hands.process(rgb_frame)
        
        # Draw hand annotations on the frame
        if results.multi_hand_landmarks:
            hands_on_ground_count = 0
            
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                if self.hands_on_ground(hand_landmarks, h):
                    hands_on_ground_count += 1
            
            # Check if both hands are on the ground
            if hands_on_ground_count >= self.MIN_HANDS_FOR_HANDSTAND:
                self.stable_frame_counter += 1
                if self.stable_frame_counter >= self.STABLE_FRAMES_REQUIRED and not self.is_timing:
                    self.start_timing()
            else:
                # If hands were on ground and now they're not, stop timing
                if self.is_timing:
                    self.stop_timing()
                self.stable_frame_counter = 0
        else:
            # No hands detected, stop timing if it was running
            if self.is_timing:
                self.stop_timing()
            self.stable_frame_counter = 0
        
        # Display timer info on frame
        self.add_timer_info(frame)
        
        # Check if maximum attempts reached and show prompt
        if len(self.timer_history) >= self.MAX_ATTEMPTS and not self.exit_prompt_shown:
            self.display_exit_prompt(frame)
            self.exit_prompt_shown = True
        
        return frame
    
    def start_timing(self):
        """Start the handstand timer"""
        self.start_time = time.time()
        self.is_timing = True
        print("Timing started!")
    
    def stop_timing(self):
        """Stop the handstand timer and record the duration"""
        if self.is_timing:
            self.end_time = time.time()
            duration = self.end_time - self.start_time
            self.timer_history.append(duration)
            self.is_timing = False
            print(f"Timing stopped! Duration: {duration:.2f} seconds")
    
    def add_timer_info(self, frame):
        """Add timer information to the frame"""
        h, w, _ = frame.shape
        
        # Current timer or last record
        if self.is_timing:
            current_time = time.time() - self.start_time
            timer_text = f"Time: {current_time:.2f} s"
            cv2.putText(frame, timer_text, (20, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif self.timer_history:
            last_time = self.timer_history[-1]
            timer_text = f"Last: {last_time:.2f} s"
            cv2.putText(frame, timer_text, (20, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Best record
        best_time = 0
        if self.timer_history:
            best_time = max(self.timer_history)
            best_text = f"Best: {best_time:.2f} s"
            cv2.putText(frame, best_text, (20, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Status indicator
        status_text = "RECORDING" if self.is_timing else "Ready"
        status_color = (0, 0, 255) if self.is_timing else (255, 255, 255)
        cv2.putText(frame, status_text, (w - 200, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
        
        # Display list of attempts on the right side
        self.display_attempt_history(frame, best_time)
        
        # Display attempt counter
        attempts_left = self.MAX_ATTEMPTS - len(self.timer_history)
        if attempts_left > 0:
            attempts_text = f"Attempts left: {attempts_left}"
            cv2.putText(frame, attempts_text, (20, h - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    def display_attempt_history(self, frame, best_time):
        """Display list of attempts on right side of frame with black background"""
        h, w, _ = frame.shape
        
        # Create a solid black background for the attempt list
        if self.timer_history:
            # Calculate box dimensions
            box_height = 40 + len(self.timer_history) * 30  # Header + attempts
            box_width = 200
            
            # Draw solid black background
            cv2.rectangle(frame, (w - box_width - 10, 130), 
                         (w - 10, 140 + box_height), (0, 0, 0), -1)
        
        # Header for attempts list
        cv2.putText(frame, "Attempts:", (w - 200, 140), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # List attempts with the best time highlighted in green
        for i, duration in enumerate(self.timer_history):
            y_pos = 170 + i * 30
            attempt_text = f"#{i+1}: {duration:.2f}s"
            
            # Highlight best time in green, others in white
            text_color = (0, 255, 0) if abs(duration - best_time) < 0.001 else (255, 255, 255)
            cv2.putText(frame, attempt_text, (w - 200, y_pos), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
    
    def display_exit_prompt(self, frame):
        """Display exit prompt after maximum attempts reached"""
        h, w, _ = frame.shape
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (int(w/4), int(h/3)), (int(3*w/4), int(2*h/3)), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Display prompt text
        prompt_text1 = "Maximum attempts reached!"
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
        """Main method to run the handstand timer"""
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        
        # Set fullscreen window
        cv2.namedWindow('Handstand Timer', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Handstand Timer', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Process the frame
            processed_frame = self.process_frame(frame)
            
            # Display the frame
            cv2.imshow('Handstand Timer', processed_frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Force exit prompt after maximum attempts
            if len(self.timer_history) >= self.MAX_ATTEMPTS:
                # Still allow user to observe their results before pressing 'q'
                pass
        
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()

if __name__ == "__main__":
    print("Starting Handstand Timer...")
    print("Position yourself so both hands are visible in the frame.")
    print("Timer will start when both hands are detected on the ground.")
    print("You have 10 attempts before the app will prompt to exit.")
    print("Press 'q' to quit.")
    
    timer = HandstandTimer()
    timer.run()