"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Date: April 7, 2023
Description: This script downloads YouTube videos in the specified quality or allows the user to select a quality from the available streams.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
## Imports
import os
os.system("title Don't mind the LOG window!")
import argparse
import ctypes
# import gui.splashscreen
from cli.CLI_VideoListManager import VideoListManagerCLI
from core.common import audio_bitrate_list, video_resolution_list, fps_value_list
from core.download_options import setOutputKeepsStr
from web.webapp import default as DefaultCFG

def hide_console():
    try:
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        HWND = user32.GetForegroundWindow()
        kernel32.FreeConsole()
        user32.ShowWindow(HWND, 0)  # SW_HIDE
    except Exception as e:
        print(f"Error hiding console: {e}")
    #end
#end

def run_cli(args):

    vlm = VideoListManagerCLI()
    # Output format definition
    outputExt = ".mkv"
    # Parameters for Analysis
    use_multithreading_analysis = args.enable_analysis_threading
    # Parameters for Download
    process_via_multithreading = args.enable_download_threading
    
    input_text = " ".join(args.urls)

    vlm.setUiDispStatus("Analysis started")
    vlm.import_valid_Youtube_videos_from_textOrURL_list( 
                text=input_text,
                use_analysis_multithreading=use_multithreading_analysis)
    vlm.setUiDispStatus("Analysis completed")

    limits = vlm.getLimitsAndPriorityFromInputArguments(args)

    if not (args.audio or args.video):
        args.combine = True
    #end

    # Set the download flags
    for item in vlm.infoList:
        item.download_status = setOutputKeepsStr(
            combined=args.combine,
            audio_only=args.audio,
            video_only=args.video,
            subtitles_only=args.subtitles,
            thumbnail=args.thumbnails,
            info=args.info,
            comments=args.comments,
            spacing=2
        )

    # Start the download
    vlm.setUiDispStatus("Download started")
    vlm.downloadAllVideoItems(process_via_multithreading=process_via_multithreading, 
                              limits=limits,
                              outputDir=args.output,
                              outputExt=outputExt)
    vlm.setUiDispStatus("Download completed")

#end

def run_web_service(args):
    from web.webapp import run_from_dispatcher as run_webapp
    run_webapp(port=args.port,output_dir=args.output,
                use_multithreading_analysis=args.enable_analysis_threading,
                process_via_multithreading=args.enable_download_threading)
#end

## Main function and also a command line parsing tool
def main():
    print("======== YouTube video downloader by JessyJP ========")

    # First stage parser for mode selection for the mode switch options
    mode_parser = argparse.ArgumentParser(description="YouTube video downloader Mode selection",add_help=False)
    mode_parser.add_argument("--gui", action="store_true", help="Run GUI")
    mode_parser.add_argument("--web", action="store_true", help="Run as web service")
    mode_parser.add_argument("--cli", action="store_true", help="Run in CLI (command line interface) mode")

    # Analysis multithreading argument
    mode_parser.add_argument("-eat", "--enable-analysis-threading", action="store_true", help="Enable multithreading for URL analysis")
    # Download multithreading argument
    mode_parser.add_argument("-edt", "--enable-download-threading", action="store_true", help="Enable multithreading for downloading videos")
    # Parse known args for the mode
    mode_args, options_argv = mode_parser.parse_known_args()


    # Second stage parser for CLI arguments
    cli_parser = argparse.ArgumentParser(description="YouTube video downloader - CLI mode")
    # CLI boolean arguments with both long and short options
    cli_parser.add_argument("-c", "--combine", action="store_true", help="Combine audio and video (default)")
    cli_parser.add_argument("-a", "--audio", action="store_true", help="Download/keep audio only")
    cli_parser.add_argument("-v", "--video", action="store_true", help="Download/keep video only")
    cli_parser.add_argument("-s", "--subtitles", action="store_true", help="Add subtitles")
    cli_parser.add_argument("-t", "--thumbnails", action="store_true", help="Download the thumbnails")
    cli_parser.add_argument("-i", "--info", action="store_true", help="Keep info")
    cli_parser.add_argument("-m", "--comments", action="store_true", help="Download the comments")
    # CLI arguments with option selection
    cli_parser.add_argument("-r", "--resolution", choices=video_resolution_list, default=video_resolution_list[0], help="Video quality maximum resolution in pixels specifier")
    cli_parser.add_argument("-f", "--fps", choices=fps_value_list, default=fps_value_list[0], help="Specify the maximum fps (frames per second)")
    cli_parser.add_argument("-b", "--bitrate", choices=audio_bitrate_list, default=audio_bitrate_list[0], help="Specify the maximum audio bitrate in kbps")
    # Output directory as an optional argument
    cli_parser.add_argument("-o", "--output", default=".", help="Output directory (default: current directory)")
    # URLs as the last argument, allowing both 'url' and 'urls'
    cli_parser.add_argument("urls", nargs="+",  metavar="URL(s)", help="One or more YouTube video URLs")


    # Second stage parser for CLI arguments
    web_parser = argparse.ArgumentParser(description="YouTube video downloader - Web Service mode")
    # Output directory as an optional argument
    web_parser.add_argument("-o", "--output", default=DefaultCFG.OUTDIR, help=f"Output directory (default: {DefaultCFG.OUTDIR})")
    # web_parser.add_argument("-o", "--output", required=True, help="Output directory (default: current directory)")
    # TODO: one of the 2 options has to be selected. Either compulsory or having a default
    # Add argument for remote storage
    # web_parser.add_argument("-rs", "--remote-storage", type=str, help="Remote storage URL or path") # TODO: disable for now, maybe remove if it remains unused
    # Add Web Service-specific arguments
    web_parser.add_argument("-p", "--port", type=int, default=DefaultCFG.PORT, help=f"Port for the web service (default: {DefaultCFG.PORT})")

    ## ======== Select a mode ========
    if mode_args.cli:
        cli_args  = cli_parser.parse_args(options_argv)
        cli_args  = argparse.Namespace(**{**vars(mode_args), **vars(cli_args)})
        run_cli(cli_args)
    elif mode_args.web:
        web_args = web_parser.parse_args(options_argv)
        web_dict = argparse.Namespace(**{**vars(mode_args), **vars(web_args)})
        run_web_service(web_dict)
    elif mode_args.gui:
        # from core.common import isDeployed, os_name
        # The gui mode is called
        # if isDeployed and os_name == 'Windows':
        #     hide_console()
        # #end    
        
        # GUI main function
        from gui.main_window import main_runGUI
        main_runGUI()
    else:
        mode_parser.print_help()
        cli_parser.print_help()
        web_parser.print_help()
    #end
#end


# This block ensures the main function runs only when 
# the script is executed directly, not when imported
if __name__ == "__main__":
    main()
#end