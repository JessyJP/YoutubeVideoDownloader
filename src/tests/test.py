import subprocess

# Variables
scriptName = './src/YouTubeDownloader.py';
quality  = "max"
url = "https://www.youtube.com/watch?v=6TWJaFD6R2s"
# url = "https://www.youtube.com/watch?v=1La4QzGeaaQ"
# url = "https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu"
outputDir = "R:/" #"./output/"

# Define the command to be executed
command = []
command.append(['python', scriptName , outputDir, url ])

# Execute the command
for cmd in command:
    subprocess.run(cmd)

