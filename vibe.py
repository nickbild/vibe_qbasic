import ftplib
import time
import os
from google import genai
from google.genai.types import ModelContent, Part, UserContent


# Login to the Win98 FTP server.
ftp = ftplib.FTP("192.168.1.137")
ftp.login("nick", "")
ftp.cwd('/c/45/qb5/qbas')

# Wait for the control file to appear.
f = open("pause.txt", 'wb')

while (True):
    # Take it easy on the Win98 FTP server.
    time.sleep(3)

    try:
        ftp.retrbinary('RETR PAUSE.TXT', f.write, 1024)
        break
    except Exception as e:
        print("Control file not found: {0}.".format(e))
        continue

f.close()

# Download the source code.
f = open("vibe.bas", 'wb')
ftp.retrbinary('RETR VIBE.BAS', f.write, 1024)
f.close()

# Get the contents of the code to use as the prompt.
prompt = ""
for line in open("vibe.bas", "r"):
    prompt += line

# Prompt a coding LLM.
client = genai.Client(api_key=os.getenv('GENAIAPI'))
chat_session = client.chats.create(
    model="gemini-2.5-flash",
    history=[
        UserContent(parts=[Part(text="""You will be supplied with Microsoft QBasic code. A special marker in the code containing the string 'VIBE' 
                                indicates the area where you are to do a code completion. Consider the context of all the code supplied, then
                                provide an appropriate completion in the area of the marker. The marker may or may not be followed by instructions to guide the
                                code you write. Return the QBasic code only, and remove the marker and any instructions associated with it.
                                Do not wrap the code in markdown or delete any existing code necessary for operation.""")]),
    ],
)
response = chat_session.send_message(prompt)

# Write the modified source code to a file.
f = open("vibe_new.bas", "w")
f.write(response.text + "\n")
f.close()

# Upload the modified source code.
f = open('vibe_new.bas','rb')
ftp.storlines('STOR VIBE.BAS', f)
f.close()

# Delete the control file so QBasic can go about its business.
while(True):
    time.sleep(1)

    try:
        ftp.delete('pause.txt')
        break
    except Exception as e:
        print("Delete failed: {0}.".format(e))
        continue


ftp.quit()
