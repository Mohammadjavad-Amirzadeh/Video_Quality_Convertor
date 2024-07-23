from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from converter import convert_video
from find_resolution import get_quality
import time
import os
import threading
import shutil
from datetime import datetime


app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    startTime = time.time_ns()
    # Check if the request has the file part
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading.'}), 400

    if file:
        filename = secure_filename(file.filename)


        '''
        part of creating changed clip folders
        '''
        # The path where uploaded files will be stored
        UPLOAD_FOLDER = './changed'#
        #UPLOAD_FOLDER = '/home/mohammadjavad/Desktop/video_converter_project/changed'
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        os.chdir(UPLOAD_FOLDER)
            
        current_time = '_'.join(str(datetime.now()).split(' '))
        new_directory = f'{filename}_clip_changed_in_{current_time}'
        os.mkdir(new_directory)
        os.chdir(f'./{new_directory}')
        UPLOAD_FOLDER = os.getcwd()
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


        '''
        part of change the qualities
        '''
        input_file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_file_path)
        video_quality = get_quality(input_file_path)
        quality_list = [1080, 720, 480, 360, 144]
        try:
            threads = []
            for i in range(len(quality_list)):
                if quality_list[i] < video_quality:
                    output_path_directory = f'{UPLOAD_FOLDER}/{quality_list[i]}p'
                    if not os.path.exists(output_path_directory):
                        os.mkdir(output_path_directory)
                    output_file = f'{output_path_directory}/output_Of_{filename}_{quality_list[i]}p.mp4'
                    thread = threading.Thread(target=convert_video, args=(input_file_path, output_file, quality_list[i]))
                    thread.start()
                    threads.append(thread)

            for thread in threads:
                thread.join()
            endTime = time.time_ns()
            os.chdir('../..')
            return jsonify({'message': 'Video conversion completed.', 
                            'Time Spend': (endTime - startTime) / (10 ** 9)})
        except:
            return jsonify({'message': 'not successful'})

if __name__ == '__main__':
    app.run(debug=True)
