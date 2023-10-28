import requests
import json

access_token = input("Enter your access token here: ")

print("MENU")
print("Test connection (0)")
print("Display user information (1)")
print("Display 5 rooms (2)")
print("Create a room (3)")
print("Send a message to a room (4)")

url = 'https://webexapis.com/v1/people/me'

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

while True:
    option = input("\nPlease choose your option: ")
    res = requests.get(url, headers=headers)

    if option == "0":
        if res.status_code == 200:
            print("Your connection is successful")
        else:
            print("Your connection is unsuccessful")

    elif option == "1":
        if res.status_code == 200:
            info = res.json()
            print("User Information")
            print(f"Display Name: {info['displayName']}")
            print(f"Nickname: {info.get('nickName', 'N/A')}")
            print(f"Emails: {', '.join(info['emails'])}")
        else:
            print("Failed to retrieve user information.")

    elif option == "2":
        url = 'https://webexapis.com/v1/rooms'
        params = {'max': '5'}
        res = requests.get(url, headers=headers, params=params)
        roomInfo = res.json()

        if res.status_code == 200:
            if 'items' in roomInfo:
                print("Rooms Information")
                for item in roomInfo['items']:
                    print(f"Room Id: {item['id']}")
                    print(f"Room name: {item['title']}")
                    print(f"Room's date created: {item['created']}")
                    print(f"Last activity: {item['lastActivity']}")
            else:
                print("No rooms found.")

    elif option == "3":
        url = 'https://webexapis.com/v1/rooms'
        roomName = input("Create a room: ")
        params = {'title': roomName}
        res = requests.post(url, headers=headers, json=params)

        if res.status_code == 200:
            print(f"Room '{roomName}' has been created.")
        else:
            print(f"Failed to create a room due to error: {res.status_code}")

    elif option == "4":
        url = 'https://webexapis.com/v1/rooms'
        params = {'max': '5'}
        res = requests.get(url, headers=headers, params=params)
        roomInfo = res.json()

        if res.status_code == 200:
            print("\tROOMS")
            print("*" * 120)
            for i, item in enumerate(roomInfo.get('items', [])):
                print(f"({i + 1}) {item['title']}")
            print("*" * 120)

            roomChoice = int(input("\nChoose a room to send a message:")) - 1

            if 0 <= roomChoice < len(roomInfo.get('items', [])):
                roomIDselected = roomInfo['items'][roomChoice]['id']
                roomNameSelected = roomInfo['items'][roomChoice]['title']
                messageToRoom = input("Enter the message you want to send: ")
                params = {'roomId': roomIDselected, 'markdown': messageToRoom}
                url = 'https://webexapis.com/v1/messages'
                res = requests.post(url, headers=headers, json=params)

                if res.status_code == 200:
                    print(f"Message '{messageToRoom}' is sent to room: {roomNameSelected}")
                else:
                    print(f"Failed to send the message due to error: {res.status_code}")

    else:
        print("Choose the right option")

    userInput = input("Press Enter to return to the main menu: ")
    if userInput.lower() == 'exit':
        break
