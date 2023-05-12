import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import subprocess
import requests
from io import BytesIO
from PIL import Image, ImageTk


class Application:
    def __init__(self, master):
        self.master = master
        master.title("Fire Detection System")

        # Fire Detection System GUI
        self.fd_frame = ttk.LabelFrame(master, text="Fire Detection System")
        self.fd_frame.grid(row=0, column=0, padx=10, pady=10)

        self.fd_output = scrolledtext.ScrolledText(self.fd_frame, width=50, height=10)
        self.fd_output.grid(row=0, column=0, padx=10, pady=10)

        self.fd_start_button = ttk.Button(self.fd_frame, text="Start", command=self.start_fd_detection)
        self.fd_start_button.grid(row=1, column=0, padx=10, pady=10)

        self.fd_stop_button = ttk.Button(self.fd_frame, text="Stop", command=self.stop_fd_detection)
        self.fd_stop_button.grid(row=1, column=1, padx=10, pady=10)

        # TCP File Receiver GUI
        self.tcp_frame = ttk.LabelFrame(master, text="Thermal sensor message")
        self.tcp_frame.grid(row=0, column=1, padx=10, pady=10)

        self.tcp_output = scrolledtext.ScrolledText(self.tcp_frame, width=50, height=10)
        self.tcp_output.grid(row=0, column=0, padx=10, pady=10)

        self.tcp_start_button = ttk.Button(self.tcp_frame, text="Start", command=self.start_tcp_receiver)
        self.tcp_start_button.grid(row=1, column=0, padx=10, pady=10)

        self.tcp_stop_button = ttk.Button(self.tcp_frame, text="Stop", command=self.stop_tcp_receiver)
        self.tcp_stop_button.grid(row=1, column=1, padx=10, pady=10)

        # Detection System Variables
        self.fd_process = None
        self.tcp_process = None

    def start_fd_detection(self):
        self.fd_output.insert(tk.END, "Starting Fire Detection System...\n")
        self.fd_output.see(tk.END)

        # Start the Fire Detection System script in a new process
        self.fd_process = subprocess.Popen(["python", "fire_detection_system.py"],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT,
                                           universal_newlines=True)

        # Start a new thread to capture and display the console output
        self.fd_thread = threading.Thread(target=self.capture_fd_output)
        self.fd_thread.start()

    def capture_fd_output(self):
        for line in iter(self.fd_process.stdout.readline, ""):
            self.fd_output.insert(tk.END, line)
            self.fd_output.see(tk.END)

    def stop_fd_detection(self):
        self.fd_output.insert(tk.END, "Stopping Fire Detection System...\n")
        self.fd_output.see(tk.END)
        self.fd_process.terminate()
        self.fd_thread.join()

    def start_tcp_receiver(self):
        self.tcp_output.insert(tk.END, "Starting TCP connection with thermal sensor...\n")
        self.tcp_output.see(tk.END)

        # Start the TCP File Receiver script in a new process
        self.tcp_process = subprocess.Popen(["python", "sensor_message.py"],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT,
                                            universal_newlines=True)

        # Start a new thread to capture and display the console output
        self.tcp_thread = threading.Thread(target=self.capture_tcp_output)
        self.tcp_thread.start()

    def capture_tcp_output(self):
        for line in iter(self.tcp_process.stdout.readline, ""):
            self.tcp_output.insert(tk.END, line)
            self.tcp_output.see(tk.END)

    def stop_tcp_receiver(self):
        self.tcp_output.insert(tk.END, "Stopping TCP connection with thermal sensor...\n")
        self.tcp_output.see(tk.END)

        # Terminate the TCP File Receiver process and thread
        self.tcp_process.terminate()
        self.tcp_thread.join()


root = tk.Tk()
app = Application(root)
root.mainloop()
