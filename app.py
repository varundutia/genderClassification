from flask import *  
import tensorflow.keras
from PIL import Image,ImageOps
import numpy as np
from keras.preprocessing import image
import os
app = Flask(__name__)  

@app.route('/')  
def upload():  
    return render_template("index.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)
        np.set_printoptions(suppress=True)
        model = tensorflow.keras.models.load_model(os.getcwd()+"/model/keras_model.h5")
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image_a = image.load_img(f.filename, target_size = (64, 64))
        size = (224, 224)
        image_a = ImageOps.fit(image_a, size, Image.ANTIALIAS)
        image_array = np.asarray(image_a)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)
        if prediction[0][0] == 1:
         prediction = 'Male'
        else:
         prediction = 'Female'  
        os.remove(os.getcwd() +"/"+ f.filename)
        return render_template("index.html", message = 'Prediction: '+prediction)  
  
if __name__ == '__main__':  
    app.run(debug = True)  