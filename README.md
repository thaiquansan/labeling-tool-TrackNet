# labeling-tool-for-TrackNet
- Link to TrackNet project: https://github.com/yastrebksv/TrackNet
- A labeling tool for TrackNet system write in Python
## Labeling Tool
This is a Python-based GUI tool for labeling images with visibility status, coordinates, and status information. It is designed to be user-friendly and allows for zooming and panning within images. This tool can be particularly useful for tasks such as labeling objects in images for machine learning projects, where precise annotations are required.

## Features
    - Image Loading: Load images from a selected folder.
    - Image Navigation: Use arrow keys to navigate through the images.
    - Zooming: Zoom in and out using the mouse wheel.
    - Annotation: Annotate images with visibility status, coordinates, and other statuses.
    - Saving Annotations: Save annotations in a CSV file with specified formats.

## Installation
1. Clone the repository:
git clone https://github.com/thaiquansan/labeling-tool-TrackNet.git

2. Creating a Virtual environment:
It is recommended to use a virtual environment to manage dependencies. Here's how to create and activate one:
- Create a Virtual Environment:
    python -m venv venv
- Activate the Virtual Environment:
    + On Windows: .\venv\Scripts\activate
    + On macOS/Linux: source venv/bin/activate

3. Installing Dependencies: Ensure you have Python installed along with the following libraries:
    - tkinter
    - Pillow (Python Imaging Library)
    - os
    - csv
You can install the required packages using pip:
pip install Pillow

Running the Tool:
To run the tool, simply execute the LabelingTool class:
    python labeling_tool.py

## Usage
1. Loading Images:
    - Click the "Select Folder" button to load images from a folder. The tool supports .png files.
    - The images will be displayed one by one in the main window.
2. Navigating Images:
    - Use the Left Arrow key to view the previous image.
    - Use the Right Arrow key to view the next image.
3. Zooming:
    Use the mouse wheel to zoom in or out on the image. 

4. Annotating Images:
    - Click on the image to add coordinates for the object.
    - Select the appropriate visibility status:
        + No Ball: No object is visible:
        + Easy Identification: Object is easily visible.
        + Hard Identification: Object is visible but not easy to identify.
        + Occluded Ball: Object is partially occluded.
    - Select the status:
        + Flying: The object is in the air.
        + Hit: The object has been hit.
        + Bouncing: The object is bouncing.

5. Saving Annotations:
Click the "Save Labels" button to save all annotations to a CSV file named Label.csv in the selected image directory.
File Format
The CSV file will have the following columns:
    - file name: Name of the image file.
    - visibility: Visibility status (0: No ball, 1: Easy Identification, 2: Hard Identification, 3: Occluded Ball).
    - x-coordinate: X-coordinate of the annotated point.
    - y-coordinate: Y-coordinate of the annotated point.
    - status: Status of the object (0: Flying, 1: Hit, 2: Bounce).

## Example CSV Output
file name,visibility,x-coordinate,y-coordinate,status  
image1.png,1,250,300,0  
image2.png,3,150,200,2  
image3.png,0,,,  

## Additional Information
- If a visibility status other than "No Ball" is selected, you must annotate the coordinates, or a warning will be shown when attempting to save the labels.
- The status radio buttons will be disabled if "No Ball" is selected.

## License
This project is open source and available under the MIT License.

## Acknowledgements
This tool was built with Python's tkinter for the GUI, and Pillow for image handling.

---------------------------------------------------------------------------------------------------

Feel free to modify this tool to suit your specific needs!
