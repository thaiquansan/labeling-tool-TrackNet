""" 
Ubuntu Linux version
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import csv

class LabelingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Labeling Tool")
        
        # Initialize variables
        self.selected_folder = None

        # Initialize variables
        self.idx = 0
        self.imgs = []
        self.Visibility = []
        self.Status = []
        self.CoordinateX = []
        self.CoordinateY = []
        self.circle = None

        self.zoom_level = 1.0
        self.zoom_min = 0.5
        self.zoom_max = 3.0

        # GUI Elements
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.label2 = tk.Label(self.frame, text="Select folder with images")
        self.label2.pack()

        self.canvas = tk.Canvas(self.frame, width=960, height=540)
        self.canvas.pack()

        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack()

        self.button1 = tk.Button(self.button_frame, text="Select Folder", command=self.load_images)
        self.button1.grid(row=0, column=0)

        self.button2 = tk.Button(self.button_frame, text="Save Labels", command=self.save_labels)
        self.button2.grid(row=0, column=1)

        # Visibility and Status radio buttons
        self.option_frame = tk.Frame(self.frame)
        self.option_frame.pack()

        self.visibility_label = tk.Label(self.option_frame, text="Visibility Status")
        self.visibility_label.grid(row=0, column=0)

        self.visibility_var = tk.IntVar()
        self.visibility_var.set(1)  # Default value
        
        self.no_ball_rb = tk.Radiobutton(self.option_frame, text="No Ball", variable=self.visibility_var, value=0, command=self.update_visibility)
        self.no_ball_rb.grid(row=0, column=1)
        self.easy_identification_rb = tk.Radiobutton(self.option_frame, text="Easy Identification", variable=self.visibility_var, value=1, command=self.update_visibility)
        self.easy_identification_rb.grid(row=0, column=2)
        self.hard_identification_rb = tk.Radiobutton(self.option_frame, text="Hard Identification", variable=self.visibility_var, value=2, command=self.update_visibility)
        self.hard_identification_rb.grid(row=0, column=3)
        self.occluded_ball_rb = tk.Radiobutton(self.option_frame, text="Occluded Ball", variable=self.visibility_var, value=3, command=self.update_visibility)
        self.occluded_ball_rb.grid(row=0, column=4)

        self.status_label = tk.Label(self.option_frame, text="Status")
        self.status_label.grid(row=1, column=0)

        self.status_var = tk.IntVar()
        self.status_var.set(0)  # Default value
        
        self.flying_rb = tk.Radiobutton(self.option_frame, text="Flying", variable=self.status_var, value=0, command=self.update_status)
        self.flying_rb.grid(row=1, column=1)
        self.hit_rb = tk.Radiobutton(self.option_frame, text="Hit", variable=self.status_var, value=1, command=self.update_status)
        self.hit_rb.grid(row=1, column=2)
        self.bouncing_rb = tk.Radiobutton(self.option_frame, text="Bouncing", variable=self.status_var, value=2, command=self.update_status)
        self.bouncing_rb.grid(row=1, column=3)

        # Bind keyboard arrows for navigation
        self.root.bind('<Left>', self.show_previous_image)
        self.root.bind('<Right>', self.show_next_image)
        # Bind mouse scroll events for Linux
        self.canvas.bind("<Button-4>", self.zoom_image_linux)
        self.canvas.bind("<Button-5>", self.zoom_image_linux)

    def create_label_file(self, folder_path):
        label_file_path = os.path.join(folder_path, 'label.csv')
        
        # Check if the label file already exists
        if not os.path.exists(label_file_path):
            with open(label_file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['filename', 'x', 'y', 'visibility', 'status'])
            messagebox.showinfo("Info", "Label file created successfully!")
        else:
            messagebox.showinfo("Info", "Label file already exists.")
            
    def load_images(self):
        dName_img = filedialog.askdirectory()
        if dName_img:
            self.selected_folder = dName_img
            self.label2.config(text=dName_img)
            self.imgs = [os.path.join(dName_img, f) for f in os.listdir(dName_img) if f.endswith('.png')]
            self.imgs.sort()

            # Initialize the lists based on the number of images
            self.Visibility = [-1] * len(self.imgs)
            self.Status = [0] * len(self.imgs)
            self.CoordinateX = [-1] * len(self.imgs)
            self.CoordinateY = [-1] * len(self.imgs)

            # Automatically create the label file if it doesn't exist
            self.create_label_file(dName_img)

            self.idx = 0
            self.show_image()

    def show_image(self):
        img = Image.open(self.imgs[self.idx])
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        self.original_img = img
        self.update_image_display()

    def update_image_display(self):
        # Resize image based on zoom level
        img = self.original_img.resize((int(1920 * self.zoom_level), int(1080 * self.zoom_level)), Image.Resampling.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
        self.label2.config(text=self.imgs[self.idx])

        # Draw circle if coordinates exist
        if self.CoordinateX[self.idx] != -1 and self.CoordinateY[self.idx] != -1:
            self.canvas.delete(self.circle)
            x = self.CoordinateX[self.idx] * self.zoom_level
            y = self.CoordinateY[self.idx] * self.zoom_level
            self.circle = self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='red', outline='red')

    # Adjust zoom_image method for Linux scroll event
    def zoom_image_linux(self, event):
        if event.num == 4:
            self.zoom_level = min(self.zoom_level + 0.1, self.zoom_max)
        elif event.num == 5:
            self.zoom_level = max(self.zoom_level - 0.1, self.zoom_min)
        self.update_image_display()

    def image_click_callback(self, event):
        x, y = event.x / self.zoom_level, event.y / self.zoom_level
        self.CoordinateX[self.idx] = x
        self.CoordinateY[self.idx] = y
        self.canvas.delete(self.circle)
        self.circle = self.canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red', outline='red')
        
        # If no visibility is selected, default to 'Easy Identification'
        if self.Visibility[self.idx] == -1:
            self.Visibility[self.idx] = 1  # Easy Identification
        
        # If no status is selected, default to 'Flying'
        if self.Status[self.idx] == 0:
            self.Status[self.idx] = 0  # Flying

    def show_previous_image(self, event):
        if self.idx > 0:
            self.idx -= 1
            self.show_image()
            self.update_ui()

    def show_next_image(self, event):
        if self.idx < len(self.imgs) - 1:
            self.idx += 1
            self.show_image()
            self.update_ui()

    def update_visibility(self):
        self.Visibility[self.idx] = self.visibility_var.get()
        if self.Visibility[self.idx] == 0:
            self.flying_rb.config(state=tk.DISABLED)
            self.hit_rb.config(state=tk.DISABLED)
            self.bouncing_rb.config(state=tk.DISABLED)
        else:
            self.flying_rb.config(state=tk.NORMAL)
            self.hit_rb.config(state=tk.NORMAL)
            self.bouncing_rb.config(state=tk.NORMAL)

    def update_status(self):
        self.Status[self.idx] = self.status_var.get()

    def update_ui(self):
        # Update radio buttons based on current image's saved state
        self.visibility_var.set(self.Visibility[self.idx])
        self.status_var.set(self.Status[self.idx])

        # Update the visibility of the status radio buttons
        if self.Visibility[self.idx] == 0:
            self.flying_rb.config(state=tk.DISABLED)
            self.hit_rb.config(state=tk.DISABLED)
            self.bouncing_rb.config(state=tk.DISABLED)
        else:
            self.flying_rb.config(state=tk.NORMAL)
            self.hit_rb.config(state=tk.NORMAL)
            self.bouncing_rb.config(state=tk.NORMAL)

        # Update the circle on the image if coordinates exist
        self.update_image_display()

    def save_labels(self):
        if self.selected_folder and os.path.isdir(self.selected_folder):
            alert = False
            for i in range(len(self.imgs)):
                # If visibility is not explicitly set, default to 'No Ball'
                if self.Visibility[i] == -1:
                    self.Visibility[i] = 0  # No Ball

                # Warn if visibility is set but coordinates are missing
                if self.Visibility[i] != 0 and (self.CoordinateX[i] == -1 or self.CoordinateY[i] == -1):
                    alert = True
                    messagebox.showwarning("Alert", f"Image {os.path.basename(self.imgs[i])} has visibility but no coordinates labeled.")
                    break
            
            if not alert:
                label_file_path = os.path.join(self.selected_folder, 'label.csv')
                with open(label_file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['file name', 'visibility', 'x-coordinate', 'y-coordinate', 'status'])
                    for i in range(len(self.imgs)):
                        fileName = os.path.basename(self.imgs[i])
                        if self.Visibility[i] == 0:
                            writer.writerow([fileName, 0, '', '', ''])
                        else:
                            writer.writerow([fileName, self.Visibility[i], self.CoordinateX[i], self.CoordinateY[i], self.Status[i]])
                messagebox.showinfo("Info", "Labels saved successfully!")
        else:
            messagebox.showerror("Error", "Please select a valid folder with images!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LabelingTool(root)
    root.mainloop()
