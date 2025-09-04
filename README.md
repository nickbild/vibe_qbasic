# QBasic Vibe Coding

Vibe coding has come to the Microsoft QBasic v1.1 IDE from 1991 with integrated LLM code completions and code generation.

![](https://raw.githubusercontent.com/nickbild/vibe_qbasic/refs/heads/main/media/logo.jpg)

## How It Works

I modified the source code of the Microsoft QBasic v1.1 IDE from 1991. While the source code is easily accessible on the web, I'm not sure about the license it is under, so I am not able to distribute any of it or provide a modified binary.

For coding assistance, the user first writes their code, then inserts a marker (`VIBE`) to specify where the model should place its focus for code completion. This marker can optionally be followed by a description of exactly what the user wants the model to do. Next, they use a new option under the search menu that I added called `Vibe it!`. It causes the code editor to be updated to reflect the changes or additions suggested by an LLM.

To make this work, I wrote a function to handle the new menu option. It is a bit of a kludge, but interfacing an early 90s IDE running on Windows 98 with a modern coding LLM is not exactly straightforward. When the `Vibe it!` option is triggered, it saves the active BAS file and then creates a flow control file. Then it pauses until that flow control file is deleted by a separate process that I will describe shortly. When resuming after the pause, the source code file is reloaded and the active window is refreshed.

A [Python script](https://github.com/nickbild/vibe_qbasic/blob/main/vibe.py) runs on a modern computer. It continually polls for the presence of the flow control file by accessing an FTP server that is running on the Windows 98 machine. Once the file appears, it moves on to download the source code file (also via FTP). Then the source code is turned into a prompt for a Gemini Flash 2.5 LLM, which is accessed via the official API. The response is written to a BAS file, which is then uploaded to the Windows 98 machine. After that, the flow control file is deleted and the IDE can take back over, reloading the source code with the updates.

Despite the complexity, it is pretty quick. Responses are generally returned in about 2 seconds.

![](https://raw.githubusercontent.com/nickbild/vibe_qbasic/refs/heads/main/media/qbasic.jpg)

## Example

**Step 1: A prompt is entered inline with the source code, then the menu item is selected.**
![](https://raw.githubusercontent.com/nickbild/vibe_qbasic/refs/heads/main/media/demo1.png)

**Step 2: The code is automatically updated to reflect the LLM's changes and additions.**
![](https://raw.githubusercontent.com/nickbild/vibe_qbasic/refs/heads/main/media/demo2.png)

**Step 3: Run it. Looks good!**
![](https://raw.githubusercontent.com/nickbild/vibe_qbasic/refs/heads/main/media/demo3.png)

## About the Author

[Nick A. Bild, MS](https://nickbild79.firebaseapp.com/#!/)
