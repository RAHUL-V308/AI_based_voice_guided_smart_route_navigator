import networkx as nx
import pyttsx3
import speech_recognition as sr
import matplotlib.pyplot as plt
import tempfile
import os
from PIL import Image
from twilio.rest import Client
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import qrcode
import io

engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture voice input
def get_voice_input(prompt):
    speak(prompt)
    with sr.Microphone() as source:
        print(prompt)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.strip().title()
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return get_voice_input(prompt)
        except sr.RequestError:
            print("Speech service is unavailable.")
            return None

# Function to generate directional route image and return the file path
def generate_directional_image(path, graph):
    plt.figure(figsize=(10, 6))
    x, y = 0, 0
    coords = [(x, y)]
    direction_map = {
        'straight': (0,1),
        'right': (1,0),
        'left': (0,-1)
    }

    for i in range(len(path) - 1):
        edge = graph.get_edge_data(path[i], path[i + 1])
        dx, dy = direction_map.get(edge['direction'], (1, 0))
        x += dx
        y += dy
        coords.append((x, y))

    for i in range(len(coords) - 1):
        x_vals = [coords[i][0], coords[i + 1][0]]
        y_vals = [coords[i][1], coords[i + 1][1]]
        plt.plot(x_vals, y_vals, 'bo-')
        plt.text(coords[i][0], coords[i][1] + 0.1, f"{path[i]}\n{graph[path[i]][path[i + 1]]['distance']}m", ha='center')

    plt.text(coords[-1][0], coords[-1][1] + 0.1, path[-1], ha='center')
    plt.axis('off')
    temp_path = os.path.join(tempfile.gettempdir(), "route.png")
    plt.savefig(temp_path)
    plt.close()

    # Display the image locally
    img = Image.open(temp_path)
    img.show()

    return temp_path

# Upload image to Google Drive and return the shareable link
def upload_to_drive(image_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'title': os.path.basename(image_path)})
    file.SetContentFile(image_path)
    file.Upload()

    file.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    })

    print(f"Uploaded to Google Drive: {file['title']}")
    return file['alternateLink']

# Generate and display QR code for a given link
def generate_qr_code(link):
    qr = qrcode.make(link)
    qr_path = os.path.join(tempfile.gettempdir(), "drive_link_qr.png")
    qr.save(qr_path)
    img = Image.open(qr_path)
    img.show()
    print(f"QR Code for Drive Link: {qr_path}")

# Function to send SMS with route text and image link
def send_sms_with_image(phone_number, route_text, image_url):
    account_sid = 'your-account-sid'
    auth_token = 'your-auth-token'
    twilio_number = 'your-twilio-number'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your route directions:\n{route_text}\n\nView image: {image_url}",
        from_=twilio_number,
        to=phone_number
    )
    print(f"Message sent! SID: {message.sid}")

# Step 1: Create the college map as a directed graph
G = nx.DiGraph()

# Step 2: Add nodes (locations) and edges (paths with direction and distance)
G.add_edge("Entrance", "CSE Dept", distance=50, direction="straight")
G.add_edge("CSE Dept", "Library", distance=100, direction="right")
G.add_edge("Library", "Hostel", distance=150, direction="left")
G.add_edge("CSE Dept", "ECE Dept", distance=60, direction="left")
G.add_edge("ECE Dept", "Auditorium", distance=90, direction="right")
G.add_edge("Library", "Canteen", distance=80, direction="right")
G.add_edge("Canteen", "Hostel", distance=70, direction="left")

# Step 3: Take voice input from the user
start = get_voice_input("Please say your starting location:")
end = get_voice_input("Please say your destination:")

# Step 4: Check if both locations exist
if not G.has_node(start) or not G.has_node(end):
    print("Invalid start or end location. Please check and try again.")
else:
    try:
        # Step 5: Find the shortest path based on distance
        path = nx.shortest_path(G, source=start, target=end, weight='distance')

        print("\nRoute directions:")
        directions = []
        for i in range(len(path) - 1):
            edge = G.get_edge_data(path[i], path[i + 1])
            p = f"From {path[i]}, turn {edge['direction']} and move {edge['distance']} metres to reach {path[i + 1]}."
            directions.append(p)
            speak(p)

        final_message = f"\nYou have arrived at your destination: {end}"
        directions.append(final_message)
        print('\n'.join(directions))
        speak(final_message)

        choice = get_voice_input("Do you want to receive this route? Say 'Yes' or 'No'.")
        if choice and 'yes' in choice.lower():
            mode = get_voice_input("Would you like to receive it by QR code or phone number?")
            speak("Generating image of your route.")
            img_path = generate_directional_image(path, G)
            speak("Uploading image to Google Drive.")
            drive_url = upload_to_drive(img_path)

            if 'qr' in mode.lower():
                speak("Generating QR code for the route image.")
                generate_qr_code(drive_url)
            else:
                phone = get_voice_input("Please say your phone number digit by digit.")
                cleaned_number = ''.join(filter(str.isdigit, phone))

                if len(cleaned_number) == 10:
                    formatted_phone = "+91" + cleaned_number
                    speak(f"Sending the route image to {formatted_phone}")
                    print(f"\U0001F4DE Formatted phone number: {formatted_phone}")
                    send_sms_with_image(formatted_phone, '\n'.join(directions), drive_url)
                else:
                    speak("Invalid phone number. It should be 10 digits. Please try again.")
                    print("❌ Invalid phone number received:", cleaned_number)

    except nx.NetworkXNoPath:
        print(f"No path found between {start} and {end}.")
