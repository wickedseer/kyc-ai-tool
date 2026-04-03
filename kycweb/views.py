"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import os
from kycweb.aadhar import crop_aadhar, get_address, get_labels_from_aadhar
from kycweb.gst import get_gst_data
from kycweb.pan import get_labels_from_pan
from kycweb.cheque import get_micrcode, ensemble_acc_output, get_ifsc, get_name
from kycweb.processing import recognise_text, preprocess_img
from kycweb.face_matching import match_faces

from kycweb import app

@app.route('/')
@app.route('/home')

def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Extractify - Login',
        year=datetime.now().year
    )

@app.route('/main', methods=['POST'])
def main():
    """Renders the main page """
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "12345678":
        return render_template(
        'home.html',
        title='Extractify',
        year=datetime.now().year)

    
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

# path to upload images
UPLOAD_FOLDER = './kycweb/UPLOAD_FOLDER/'

# route to uploading images of id cards
@app.route('/upload', methods=['POST'])

def index():
    
    if request.method == 'POST':
        
        current_time = str(datetime.now()).replace('-', '_').replace(':', '_')

        # get the type of image that is being received
        image_type = request.form['type']
        
        # setting filename that is being received to current time stamp with its directory
        filename = UPLOAD_FOLDER + image_type + '/' + current_time + '.png'
        preprocessed_filename = UPLOAD_FOLDER + image_type + '/' + current_time + '_preprocessed' + '.png'

        # if the image_type folder doesn't already exist, create it
        if not os.path.exists(UPLOAD_FOLDER + image_type):
            os.mkdir(UPLOAD_FOLDER + image_type)
            # directory for saving faces in the id cards
            os.mkdir(UPLOAD_FOLDER + image_type + '/' + 'faces')
            os.mkdir(UPLOAD_FOLDER + image_type + '/' + 'signature')
        
        # if image_type is bank cheque, preprocess accordingly
        if image_type == 'Cheque':
            details = {}

            # get photo from android
            photo = request.files['photo']
            photo.save(filename)

            preprocess_img(filename, preprocessed_filename)

            # get details from the image
            details['MICR'] = get_micrcode(filename)
            details['ACC.No'] = ensemble_acc_output(preprocessed_filename)
            details['IFSC'] = get_ifsc(preprocessed_filename)
            
            data, p = recognise_text(preprocessed_filename, "", "")
            details['Name'] = get_name(data)

            # return the details and the image name it is saved as
            return jsonify({'status':True, 'fields': details, 'image_path': filename})

        elif image_type == 'Aadhar Back':
            details = {}

            # get photo from android
            photo = request.files['photo-pan']
            photo.save(filename)
            

            preprocess_img(filename, preprocessed_filename)

            crop_path = UPLOAD_FOLDER + image_type + '/temp/' + current_time + '.png'

            if not os.path.exists(UPLOAD_FOLDER + image_type + '/temp'):
                os.mkdir(UPLOAD_FOLDER + image_type + '/temp')

            crop_aadhar(preprocessed_filename, crop_path)

            # recognise text in the id card
            data, photo_path = recognise_text(crop_path, "", filename)
            
            details = get_address(data)

            os.remove(crop_path)

            # return the details and the image name it is saved as
            return jsonify({'status':True, 'fields': details, 'image_path': filename})
        
        else:
            # setting directory for saving face in the id card
            photo_path = UPLOAD_FOLDER + image_type + '/' + 'faces' + '/' + current_time + '.png'
            sign_path = UPLOAD_FOLDER + image_type + '/' + 'signature' + '/' + current_time + '.png'

            # get photo from android
            if image_type == 'PAN':
                photo = request.files['photo-pan']
                photo.save(filename)
            elif image_type == 'Aadhar':
                photo = request.files['photo-aadhar']
                photo.save(filename)
            else:
                photo = request.files['photo-gst']
                photo.save(filename)
           

            preprocess_img(filename, preprocessed_filename)

            # recognise text in the id card
            data, photo_path = recognise_text(preprocessed_filename, photo_path, filename, sign = sign_path)
            
            # extract labels from the recognised text according to the image_type
            if image_type == "Aadhar":
                details = get_labels_from_aadhar(data)
            elif image_type == "PAN":
                details = get_labels_from_pan(data)
            elif image_type == "GST":
                details = get_gst_data(data)
            else:
                details = { idx : text for idx, text in enumerate(data) }

            with open('outputs.txt', 'a+') as f:
                f.write("##########################################################################\n\n")
                f.write('######################## Raw Output #############################\n\n')
                for value in data:
                    f.write(str(value) + '\n')
                f.write('\n\n######################## Cleaned Output #############################\n\n')
                for key, value in details.items():
                    f.write(str(key) + ' : ' + str(value) + '\n')
                f.write("##########################################################################\n\n")

            # return the details and the image name and photo path it is saved as
            return jsonify({'status':True, 'fields': details, 'image_path': filename, 'photo_path': photo_path, 'sign_path': sign_path})
    else:
        # if not POST, terminate
        return jsonify({'status':False})


@app.route('/face_match',methods=['GET','POST'])
def face_match():

    # saving current timestamp
    current_time = str(datetime.datetime.now())

    # temporary folder for saving face for face matching
    if not os.path.exists(UPLOAD_FOLDER + 'temp'):
            os.mkdir(UPLOAD_FOLDER + 'temp')

    # setting filename that is being received to current time stamp with its directory
    filename = UPLOAD_FOLDER + 'temp' + '/' + current_time + '.png'
    
    # getting the path of the saved face image
    photo_path = request.form['photopath']

    # get live face from android
    photo = request.files['liveface']
    photo.save(filename)
    
    # check face match and probability
    result, percent = match_faces(id_card_image=photo_path, ref_image=filename)

    # delete the temp face image
    os.remove(filename)

    # return face match prediction and percentage
    return jsonify({'status':str(result), 'percent': percent})
