import pyrebase

config = {
    "apiKey": "AIzaSyAwndMaKfN6cC82WSDOvbRCHDci8pUD-sU",
    "authDomain": "flutterapp-7cd19.firebaseapp.com",
    "databaseURL": "https://flutterapp-7cd19-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "flutterapp-7cd19",
    "storageBucket": "flutterapp-7cd19.appspot.com",
    "messagingSenderId": "788331343001",
    "appId": "1:788331343001:web:ce601149aea697dae05c08",
    "measurementId": "G-QVDPJ4Y6TG"
}

firebase = pyrebase.initialize_app(config)

database = firebase.database()