# Module imports
from flask import Flask
from web.server_mgr import vlm
from web.routes import router


def main(port:int=80, output_dir:str='',
         use_multithreading_analysis:bool = False,
         process_via_multithreading:bool = False ):

    vlm.use_multithreading_analysis = use_multithreading_analysis
    vlm.process_via_multithreading = process_via_multithreading  
    vlm.setDownloadDir(output_dir)

    prefix = " -- Param: "
    print(f"{prefix}Use multithreading analysis set to: [{use_multithreading_analysis}]")
    print(f"{prefix}Use process download and mux via multithreading set to: [{process_via_multithreading}]")
    print(f"{prefix}Port set to: [{port}]")
    print(f"{prefix}Output directory set to [{output_dir}]")

    # Flask application setup
    app = Flask(__name__)
    app.secret_key = 'my_session_secret_key'  # Set a secret key for session management
    app.register_blueprint(router)

    app.run(debug=True, port=port)

if __name__ == '__main__':
    main()
#end