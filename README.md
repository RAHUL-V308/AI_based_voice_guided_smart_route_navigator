# AI-Based Voice-Guided College Route Assistant 🎧🗘️

This project is an intelligent assistant that helps users navigate through a college campus using **voice input**, **directional maps**, and **SMS/QR sharing**. It integrates speech recognition, route visualization, and external APIs to deliver an interactive navigation experience tailored for educational campuses.

## 🚀 Features

* 🎤 **Voice-activated navigation** – Users can speak their start and end locations.
* 📍 **Shortest path guidance** – Calculates the shortest route between locations using NetworkX.
* 🗘️ **Visual route generation** – Generates a directional map with labels and distances.
* 🔗 **Google Drive Integration** – Uploads the route map and creates a shareable link.
* 📲 **SMS Sharing with Twilio** – Sends route directions and map to a phone number.
* 🔳 **QR Code Generation** – For quick access to the map via smartphone scanning.
* 🧠 **Speech synthesis** – Speaks each step of the directions clearly.
* ✅ **Error handling & input validation** – Ensures robustness in user interaction.

## 🛠️ Technologies Used

* Python 3
* SpeechRecognition
* pyttsx3 (Text-to-Speech)
* matplotlib (Map Drawing)
* networkx (Shortest Path)
* qrcode (QR Code Generator)
* PIL (Image Display)
* GoogleDrive API (PyDrive)
* Twilio API (SMS Service)

## 🎥 How It Works

1. The user speaks their **starting point** and **destination**.
2. The system finds the shortest route and **speaks each direction**.
3. A **visual map** is created and uploaded to **Google Drive**.
4. The user chooses whether to:

   * **Receive the map via SMS**, or
   * **Get a QR code** to scan and view the map.
5. The user is guided step-by-step with clear instructions.

## 🧪 Sample Locations (Customizable)

* Entrance
* CSE Dept
* Library
* Hostel
* ECE Dept
* Auditorium
* Canteen

Note:You can expand the map by editing the graph in the code.
⚠️ Create your own client_secrets.json file by following the PyDrive Quickstart and place it in the root directory of the project.

## 📦 Setup Instructions

### 1. Install Dependencies

```bash
pip install networkx matplotlib pyttsx3 SpeechRecognition pydrive qrcode pillow twilio
```

### 2. Setup APIs

* **Google Drive API**

  * Follow [this PyDrive tutorial](https://pythonhosted.org/PyDrive/quickstart.html) to authenticate.
* **Twilio API**

  * Create an account at [twilio.com](https://www.twilio.com/)
  * Update your SID, Auth Token, and Phone Number in the script.

## 📷 Example Output

![image](https://github.com/user-attachments/assets/15d6bd05-cad7-467c-bbe3-19f3c3034aa8)
![route_qr](https://github.com/user-attachments/assets/31c54460-0ac8-4090-9008-8954afb80f5c)


## 🤖 Future Improvements

* Add a GUI using Tkinter or Flask web interface
* Support for multiple campus maps
* Multilingual voice support (Tamil, Hindi, etc.)
* Integration with GPS devices

## 💡 Acknowledgements

* [PyDrive Documentation](https://pythonhosted.org/PyDrive/)
* [Twilio Python SDK](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account)
* [SpeechRecognition Python Library](https://pypi.org/project/SpeechRecognition/)

## 🙇‍♂️ Author

Made with ❤️ by **Rahul V**
3rd Year CSE Student, K. S. Rangasamy College of Technology

*If you found this project useful, feel free to star it and share!*
