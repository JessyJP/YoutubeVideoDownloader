import subprocess

# Variables
scriptName = './src/YouTubeDownloader.py';
args = []
args.append('--cli')

# Select mode
# args.append('--web')
# args.append('--gui')

# Output dir
# args.append("--output R:/") #"./output/"
args.append("-o")
args.append("R:/") #"./output/"

# quality  = "max"
args.append("-c")

# Arguments URL(s)
args.append("https://www.youtube.com/watch?v=6TWJaFD6R2s")
args.append("https://www.youtube.com/watch?v=1La4QzGeaaQ")
args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")
args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")
args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")
args.append("https://www.youtube.com/watch?v=77GWlSiwKI4" )
args.append('''https://www.youtube.com/watch?v=77GWlSiwKI4
            https://www.youtube.com/watch?v=DNsLLrCgK0U
            random_string_1234    
            https://www.youtube.com/playlist?list=PLbpi6ZahtOH6GomiNz1MJDa2aQOeFiMKH
            random_string_aaaaaaaaaaaaaaaaaaaa
            ''')
args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")
args.append("https://www.youtube.com/playlist?list=PLbpi6ZahtOH6GomiNz1MJDa2aQOeFiMKH")
args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")
args.append("https://www.youtube.com/watch?v=7n16Yw51xkI&list=PLLgJJsrdwhPxa6-02-CeHW8ocwSwl2jnu")

# Define the command to be executed
command = []
command.append(['python', scriptName,*args ])
# command.append(['python', scriptName , outputDir, url ])

# Execute the command
for cmd in command:
    subprocess.run(cmd)

