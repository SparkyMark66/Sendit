import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import socket
import threading
import os

# --- Configuration ---
# Using a non-common UDP port to avoid conflicts.
UDP_PORT = 61991
# Using the broadcast address to send data to all devices on the network.
BROADCAST_ADDR = '<broadcast>'
# Define the buffer size for receiving data. 4096 bytes = 4KB.
BUFFER_SIZE = 4096
# Define the character encoding for network transmission.
ENCODING = 'utf-8'

class DataSharerApp:
    """
    A cross-platform application for sharing text data over a local network using UDP.
    """

    def __init__(self, root):
        """
        Initializes the main application window and its components.
        """
        self.root = root
        self.root.title("Cross-Platform Data Sharer")
        self.root.geometry("700x800")
        self.root.minsize(500, 400)

        # --- UI Styling ---
        self.bg_color = "#f0f0f0"
        self.button_color = "#e1e1e1"
        self.text_bg_color = "#ffffff"
        self.font_family = "Arial"
        self.font_size = 10

        self.root.configure(bg=self.bg_color)

        # --- Main Frame ---
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg=self.bg_color)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Sending Section ---
        send_frame = tk.LabelFrame(main_frame, text="Send Text", padx=10, pady=10, bg=self.bg_color, font=(self.font_family, 12))
        send_frame.pack(pady=10, fill=tk.X)

        self.send_text = scrolledtext.ScrolledText(send_frame, wrap=tk.WORD, height=10, bg=self.text_bg_color, font=(self.font_family, self.font_size))
        self.send_text.pack(expand=True, fill=tk.BOTH)

        send_button_frame = tk.Frame(send_frame, bg=self.bg_color)
        send_button_frame.pack(fill=tk.X, pady=(5, 0))

        self.send_button = tk.Button(send_button_frame, text="Send", command=self.send_data, bg=self.button_color, font=(self.font_family, self.font_size))
        self.send_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.load_button = tk.Button(send_button_frame, text="Load from File", command=self.load_from_file, bg=self.button_color, font=(self.font_family, self.font_size))
        self.load_button.pack(side=tk.LEFT)

        # --- Receiving Section ---
        receive_frame = tk.LabelFrame(main_frame, text="Received Text", padx=10, pady=10, bg=self.bg_color, font=(self.font_family, 12))
        receive_frame.pack(pady=10, expand=True, fill=tk.BOTH)

        self.receive_text = scrolledtext.ScrolledText(receive_frame, wrap=tk.WORD, state='disabled', bg=self.text_bg_color, font=(self.font_family, self.font_size))
        self.receive_text.pack(expand=True, fill=tk.BOTH)

        receive_button_frame = tk.Frame(receive_frame, bg=self.bg_color)
        receive_button_frame.pack(fill=tk.X, pady=(5, 0))

        self.save_button = tk.Button(receive_button_frame, text="Save to File", command=self.save_to_file, bg=self.button_color, font=(self.font_family, self.font_size))
        self.save_button.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_button = tk.Button(receive_button_frame, text="Clear", command=self.clear_ui, bg=self.button_color, font=(self.font_family, self.font_size))
        self.clear_button.pack(side=tk.LEFT)

        # --- Network Setup ---
        self.setup_socket()

        # Start listening for incoming messages in a separate thread
        self.listen_thread = threading.Thread(target=self.listen_for_data, daemon=True)
        self.listen_thread.start()

        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_socket(self):
        """
        Creates and configures the UDP socket for network communication.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Enable broadcasting
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # Allow reusing the address to run multiple instances on the same machine
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind to all available interfaces on the specified port
            self.sock.bind(('', UDP_PORT))
        except OSError as e:
            messagebox.showerror("Socket Error", f"Failed to set up the socket: {e}\n\nAnother application might be using port {UDP_PORT}.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred during socket setup: {e}")
            self.root.destroy()

    def send_data(self):
        """
        Sends the text from the input box over the network.
        """
        message = self.send_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Empty Message", "Cannot send an empty message.")
            return

        try:
            # Encode the message and send it to the broadcast address
            self.sock.sendto(message.encode(ENCODING), (BROADCAST_ADDR, UDP_PORT))
            self.update_received_text(f"[SENT]: You sent a message.\n")
        except Exception as e:
            messagebox.showerror("Send Error", f"Failed to send data: {e}")

    def listen_for_data(self):
        """
        Listens for incoming UDP packets and displays them in the received text area.
        This function runs in a separate thread.
        """
        while True:
            try:
                data, addr = self.sock.recvfrom(BUFFER_SIZE)
                # Decode the message and schedule the UI update on the main thread
                message = data.decode(ENCODING)
                # We use `schedule_update` to safely update the Tkinter UI from this background thread.
                self.root.after(0, self.update_received_text, f"[{addr[0]}]:\n{message}\n\n")
            except Exception:
                # This can happen when the socket is closed.
                break

    def update_received_text(self, message):
        """
        Appends a message to the received text area.
        This method is designed to be called from the main GUI thread.
        """
        self.receive_text.config(state='normal')
        self.receive_text.insert(tk.END, message)
        self.receive_text.config(state='disabled')
        self.receive_text.see(tk.END) # Auto-scroll to the bottom

    def clear_ui(self):
        """
        Clears both the sending and receiving text areas.
        """
        self.send_text.delete("1.0", tk.END)
        self.receive_text.config(state='normal')
        self.receive_text.delete("1.0", tk.END)
        self.receive_text.config(state='disabled')

    def save_to_file(self):
        """
        Saves the content of the received text area to a local file.
        """
        content = self.receive_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Nothing to Save", "The received text area is empty.")
            return

        # Open a file dialog to choose where to save the file
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Received Text"
        )
        if not filepath:
            return  # User cancelled the dialog

        try:
            with open(filepath, 'w', encoding=ENCODING) as f:
                f.write(content)
            messagebox.showinfo("Success", f"File saved successfully to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to save file: {e}")

    def load_from_file(self):
        """
        Loads text from a local file into the sending text area.
        """
        filepath = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Load Text to Send"
        )
        if not filepath:
            return # User cancelled the dialog

        try:
            with open(filepath, 'r', encoding=ENCODING) as f:
                content = f.read()
            
            # Check if the content is too large
            if len(content.encode(ENCODING)) > BUFFER_SIZE:
                 messagebox.showwarning("File Too Large", f"The file content exceeds the {BUFFER_SIZE / 1024:.0f}KB limit for a single UDP packet and may be truncated by the receiver.")

            self.send_text.delete("1.0", tk.END)
            self.send_text.insert(tk.END, content)
            messagebox.showinfo("Success", "File loaded successfully.")
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to load file: {e}")

    def on_closing(self):
        """
        Handles the application cleanup when the window is closed.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.sock.close()
            self.root.destroy()

# --- Main execution block ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DataSharerApp(root)
    root.mainloop()
