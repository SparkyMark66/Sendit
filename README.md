# **Sendit a Cross-Platform Data Sharer**

A simple, fast, and easy-to-use desktop application for sharing text and small files across computers on your local network. No cloud services, no sign-ups, just direct peer-to-peer sharing.

![Alt image of the utility]([image-url](https://github.com/SparkyMark66/Sendit/blob/main/sendit.png))

## **Features**

* **Cross-Platform:** Works on Windows, macOS, and Linux.  
* **Targeted & Broadcast Sending:** Send text to a specific computer using its IP address/hostname, or broadcast to all computers on the network running the app.  
* **Send & Receive:** A clear, two-panel interface for sending and receiving text.  
* **File Integration:** Load text from a file to send, and save received text to a file.  
* **No Installation:** Runs as a single Python script. No complex setup required.  
* **Secure on Your Network:** All data stays within your local network.

## **Requirements**

* **Python 3:** You must have Python 3 installed on your computer. You can download it from [python.org](https://www.python.org/downloads/). During installation on Windows, make sure to check the box that says **"Add Python to PATH"**.

## **How to Run the Application**

1. **Download the Code:**  
   * Go to the GitHub repository page https://github.com/SparkyMark66/Sendit.  
   * Click the green \<\> Code button.  
   * Click Download ZIP.  
   * Extract the ZIP file to a location you can easily access (e.g., your Desktop).  
2. **Open a Terminal (or Command Prompt):**  
   * **Windows:** Press Win \+ R, type cmd, and press Enter.  
   * **macOS:** Open Launchpad and search for Terminal.  
   * **Linux:** Press Ctrl \+ Alt \+ T or search for Terminal in your applications.  
3. **Navigate to the Directory:**  
   * In the terminal, use the cd (change directory) command to go to the folder where you extracted the code. For example:  
     \# Example if you saved it to your Desktop  
     cd Desktop/sendit 

4. **Run the Script:**  
   * Type the following command and press Enter:  
     python data\_sharing\_app.py

   * The application window should now appear\! Run the same script on another computer on your network to start sharing.

## **How to Use**

* **Target IP / Hostname:**  
  * To send to *all* computers on the network running the app, leave this as \<broadcast\>.  
  * To send to a *specific* computer, type its local IP address (e.g., 192.168.1.15) or its hostname (e.g., living-room-pc) into this field.  
* **Send Text:** Type or paste text into the top box and click Send.  
* **Load from File:** Click this to open a file browser. Select a .txt file to load its contents into the "Send Text" box.  
* **Received Text:** All incoming messages will appear in the bottom box, labeled with the sender's IP address.  
* **Save to File:** Click this to save the entire contents of the "Received Text" box to a .txt file.  
* **Clear:** Wipes the text from both the sending and receiving boxes.
