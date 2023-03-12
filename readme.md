# OpenAI Assistant Interface
This is a Python-based interface for interacting with the OpenAI GPT-3 assistant API using audio input from a microphone. It's a fun project that I've been working on to explore the capabilities of the OpenAI API and experiment with voice input.

I'm always looking for ways to improve the code and welcome anyone with programming skills to contribute and make it better. Feel free to fork the project and submit pull requests with your improvements.

To get started with the interface, simply install the required Python packages and follow the instructions below.


## Linux/macOS
To use the program, you will need to have [ffmpeg](https://ffmpeg.org/download.html) installed on your system.  installed on your macOS or Linux system. The program was tested on macOS Monterey Version 12.6.3, but should work on earlier versions of macOS as well.

To install the required Python packages on Linux or macOS, simply run the following command:

    pip install -r requriements.txt

Once the packages are installed, you can run the program with the following command:

    python main.py.

Before running the program, make sure that there is a config.cfg file in the root folder with your OpenAI API key inside. The file should look like this:

    [auth]
    OPENAI_API_KEY=<your-KEY>

Note: Replace <your-KEY> with your actual OpenAI API key.

## Windows

1. For Windows, it's recommended to use a virtual environment and Python 3.10, which you can download from https://www.python.org/downloads/release/python-3109/. Download directly: [Windows installer (64-bit)](https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe). Then install this Python version on your system but you do NOT want to add the new python to your PATH if you have already another Python version installed on your system. Download the speechrec repository and navigate to the root folder of the project and create a new virtual environment with the following command, replacing USERNAME with your own username:

        C:\Users\USERNAME\AppData\Local\Programs\Python\Python310\python.exe -m venv venv
    and then activate the environment:

        .\venv\Scripts\activate


2. Make sure to install FFmpeg on your system if you haven't already. 
    <details>
    <summary>How to Install FFmpeg on Windows</summary>
    as part of a larger installation
    Visit the [FFmpeg website](https://ffmpeg.org/download.html) and download the latest Windows build version that matches your system (64-bit). Or go directly to [BtbN](https://github.com/BtbN/FFmpeg-Builds/releases) and download [ffmpeg-master-latest-win64-gpl.zip
    ](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip)

    Extract the downloaded archive into a folder of your choice. It is recommended to keep the folder path short to avoid issues with long file names.

    Add the path to the FFmpeg folder to the system environment variable "Path". To do this, follow these steps:
    - Right-click on "Computer" and select "Properties".
    - Click on "Advanced system settings".
    - Click on "Environment Variables".
    - Under "System variables", look for the variable "Path" and click on "Edit".
    - Click on "New" and enter the path to the FFmpeg folder (e.g. "C:\ffmpeg\bin").
    - Click on "OK" to close all windows.

    Test that the installation was successful by opening a command prompt and typing ffmpeg -version. If the installation was successful, you should see the version information for FFmpeg displayed in the command prompt.

    Note: If you encounter any issues during installation or use of FFmpeg, refer to the official FFmpeg documentation or search for solutions online.
    </details>

3. To install the required Python packages, run the following command:

        pip install -r requriements.txt

4. You can then run the program with the following command:

        python main.py.

    If you encounter a Visual C++ runtime error, just install the components as suggested with the downloadlink: https://aka.ms/vs/16/release/vc_redist.x64.exe.

    If you encounter any problems with the local Whisper installation, follow the instructions in the readme: https://github.com/openai/whisper.
