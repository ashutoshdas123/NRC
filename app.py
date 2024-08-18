
from flask import Flask, render_template, request
import clarifai
import re
import base64

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    # request.form holds form data submitted via POST request.
    # image is the key through which you access the form data. as you uploaded in formData.append()
    image_data=request.form['image']
    
    '''decode the image data'''
    # removes the prefix and leaves only the actual image data. the cleaned up string can then be decoded and saved in a file
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    # it decodes it back to original data
    image_data = base64.b64decode(image_data)
    
    '''create a unique file name'''
    filename = 'static/images/captured_image.png'
    
    '''save the image'''
    with open(filename, 'wb') as f:
        f.write(image_data)

    return 'Photo saved successfully', 200

def process_with_clarifai():
    # initialize the clarifai app
    clarifai_app = clarifai.App(api_key='YOUR_API_KEY')
    # choose the model
    model=clarifai_app.models.get('general-v1.3')
    
    '''  '''
    filename = 'static/images/captured_image.png'
    
    prompt='this is the prompt'
    
    # Predict the contents of the image
    response=model.predict_by_filename(filename, model_options={'text': prompt})
    
    # Extract and return the necessary information from the response
    # Here you can customize what you want to return
    concepts = response['outputs'][0]['data']['concepts']
    output = [concept['name'] for concept in concepts]
    
    return {'prompt': prompt, 'predictions': output}

if __name__ == '__main__':
    app.run(debug=True)