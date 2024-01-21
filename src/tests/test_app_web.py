"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Year: 2024
Description: This script downloads YouTube videos in the specified quality or allows the user to select a quality from the available streams.

MIT License

Copyright (c) 2024 JessyJP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import subprocess

# Variables
scriptName = './src/YouTubeDownloader.py';
args = []

# Select mode
# args.append('--cli')
# args.append('--gui')
args.append('--web')

# Threading modes
args.append('--enable-analysis-threading')
args.append('--enable-download-threading')

# Output dir
# args.append("--output R:/") #"./output/"
args.append("-o")
args.append("R:/") #"./output/"

args.append("--port")
args.append("80")

# quality  = "max"
# args.append("-c")

# Arguments URL(s)
# args.append("https://www.youtube.com/watch?v=6TWJaFD6R2s")
# args.append("https://www.youtube.com/watch?v=1La4QzGeaaQ")
# args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")
# args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")
# args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")
# args.append("https://www.youtube.com/watch?v=77GWlSiwKI4" )
# args.append('''https://www.youtube.com/watch?v=77GWlSiwKI4
#             https://www.youtube.com/watch?v=DNsLLrCgK0U
#             random_string_1234    
#             https://www.youtube.com/playlist?list=PLbpi6ZahtOH6GomiNz1MJDa2aQOeFiMKH
#             random_string_aaaaaaaaaaaaaaaaaaaa
#             ''')
# args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")
# args.append("https://www.youtube.com/playlist?list=PLbpi6ZahtOH6GomiNz1MJDa2aQOeFiMKH")
# args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")
# args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")

# Define the command to be executed
command = []
command.append(['python', scriptName,*args ])
# command.append(['python', scriptName , outputDir, url ])

# Execute the command
for cmd in command:
    subprocess.run(cmd, shell=True)

