# Face Recognition Attendance System

## System Overview
The Face Recognition Attendance System provides an efficient and automated way to track attendance using computer vision. The system captures faces through a webcam, registers them with a corresponding name, and later recognizes these faces to mark attendance with a timestamp. The project offers multiple machine learning backends for recognition: K-Nearest Neighbors (KNN), Random Forest, and a built-in deep learning model via `face_recognition`.

## Tech Stack
- **Python**: Core programming language.
- **OpenCV**: Computer vision library used for image capture, grayscale conversion, and face detection (using Haar Cascades).
- **scikit-learn**: Machine learning library used for training K-Nearest Neighbors (KNN) and Random Forest classifiers.
- **face_recognition** & **dlib**: Deep-learning-based libraries used for highly accurate facial embeddings and matching.
- **win32com**: Windows COM interface for Text-to-Speech (TTS) auditory feedback.
- **NumPy / Pickle / CSV**: Data handling, serialization, and storage formats.

## Where to Use
This system is highly adaptable and can be deployed in various domains:
- **Educational Institutions**: Schools and universities can automate daily classroom attendance.
- **Corporate Workplaces**: Companies can use it for employee check-ins and check-outs at the entrance.
- **Events & Conferences**: Organizers can quickly track registered attendees without manual ticketing.
- **Restricted Access Areas**: Can act as a lightweight monitoring tool to log who has entered a specified zone.

## Workflow Explained

```mermaid
flowchart TD
    subgraph Phase1["Phase 1: Data Collection"]
        direction TB
        A(["User runs add_faces.py"]) --> B["Webcam detects & captures 100 face images"]
        B --> C["Crop, resize (50x50), and flatten images"]
        C --> D[("Store in pickle files\n(data/faces_data.pkl & names.pkl)")]
    end

    subgraph Phase2["Phase 2: Model Training & Prediction"]
        direction TB
        D --> E{"Choose Recognition Backend"}
        E -->|python knn.py| F["Train K-Nearest Neighbors (KNN)"]
        E -->|python random_forest.py| G["Train Random Forest"]
        E -->|python main.py| H["Deep Encodings via face_recognition"]
        
        F --> I["Start live webcam stream"]
        G --> I
        H --> I
        
        I --> J["Detect & Identify Face Identity"]
    end

    subgraph Phase3["Phase 3: Attendance Logging"]
        direction TB
        J --> K{"Is identity verified?"}
        K -->|Yes, User presses 'o'| L["Log Name & Timestamp to CSV"]
        L --> M((("Play audio confirmation via pywin32")))$$$
    end
    
    Phase1 --> Phase2
    Phase2 --> Phase3
```

1. **Data Collection (`add_faces.py`)**: 
   - Uses OpenCV to detect faces via a webcam.
   - Captures and crops exactly 100 face images per person.
   - Resizes and flattens these images, then stores them along with the user's name in pickle files (`data/faces_data.pkl` and `data/names.pkl`).
2. **Model Training & Prediction**:
   - Depending on the script chosen (`knn.py` or `random_forest.py`), a machine learning model is dynamically trained on the pickled data.
   - Alternatively, if `main.py` is executed, the system calculates deep facial encodings from a `Training_images` directory.
   - During the recognition phase, frames from live webcam footage are processed to detect faces, which are then passed to the trained machine learning model to predict the user identity.
3. **Attendance Logging**:
   - Once a face is recognized, the system notes the time and logs the user's name and timestamp into a CSV file (either `Attendance_DD-MM-YYYY.csv` or `Attendance.csv`).
   - The system uses voice feedback to aurally confirm that attendance has been marked.

## How to Setup

### Prerequisites
- Operating System: Windows (due to the `win32com` requirement for audio).
- Python 3.7+ installed.
- A functional webcam.

### Installation Steps
1. **Clone or Download the Project**: Ensure all the files are extracted into a single folder.
2. **Install Dependencies**: Open a terminal in the project directory and install the required modules.
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The `face_recognition` and `dlib` libraries require CMake and C++ compiler/build tools installed on your Windows machine.)*
3. **Directory Setup**:
   - Ensure the `data/` folder exists in the root directory (this is where `.xml` Haar Cascade files and `.pkl` data will be stored).
   - Ensure you download the `haarcascade_frontalface_default.xml` file into the `data/` folder if it is missing.
   - Create a `Training_images/` directory if you plan to use `main.py` directly.

## How to Use

### 1. Register a Person
Run the data collection script to record a new face:
```bash
python add_faces.py
```
- Enter the person's name when prompted in the terminal.
- Look directly into the webcam until 100 frames are captured. (Press `q` to quit early if needed).

### 2. Start the Attendance System
Run any of the recognition scripts depending on the preferred algorithm:
```bash
# To use the K-Nearest Neighbors model
python knn.py

# To use the Random Forest model
python random_forest.py

# To use deep learning based face_recognition
python main.py
```
- A webcam window will open displaying detected faces and predicted names.
- When your face is identified, press the `o` key to log your attendance into the CSV file. You will hear an audio confirmation.
- Press `q` to close the webcam window and stop the program.
