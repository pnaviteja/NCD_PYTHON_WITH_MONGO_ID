
from flask import Flask, render_template, redirect, request
from pymongo import MongoClient 
from random import randint


app = Flask(__name__, template_folder='templates')

firstname = " "
add = 0
res = " "
patient_id=" "

@app.route('/', methods=['GET',"POST"])
def reg():
    return render_template('register.html')
    

@app.route('/register', methods=['GET',"POST"]) 
def register():
    global firstname
    lastname = " "
    gender = " "
    birthday = " "
    pincode = " "
    #patient_id=0
    patient_id = randint(10000000000000,99999999999999)
    print(patient_id)
    if request.method == "POST":
    
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        birthday = request.form['birthday']
        pincode = request.form["pin"]
        #patient_id=randompatient_id(14)
        
        Collection.insert_one(
            { "patient_id":patient_id,
                "firstname" : firstname,
        "lastname":lastname,
        "gender":gender,
        "birthday":birthday,
        "pincode":pincode,
       }
        )
    return render_template('navi.html',id = patient_id)

    

@app.route('/navi', methods=['GET',"POST"])
def home():
    
    if request.method == "POST":
        
        while True:
            first = request.form.get('first')
            second = request.form.get('second')
            third = request.form.get('third')
            fourth = request.form.get('fourth')
            fifth = request.form.get('fifth')
            sixth = request.form.get('sixth')
            Collection.update_one(
                {"firstname":firstname},
            {"$set": {"first" :first,
            'second': second,
             "third":third,
            "fourth":fourth,
            "fifth":fifth,
            "sixth":sixth}}
       
        )
            score = float(first) + float(second)+float(third)+float(fourth) + float(fifth)+float(sixth)
            global add
            add=score  
            global res
            if score>4:
                res="screening needed"
                Collection.update_one(
                {"firstname":firstname},
                {"$set": {"total_count" :add}})
            else:
                res="no need to screen"
                Collection.update_one(
                {"firstname":firstname},{"$set": {"total_count" :add}})
            return render_template('result.html', add1=add,res=res)
    return render_template('navi.html')



@app.route('/back',methods=['POST','GET'])
def back():
    if request.method=='POST':
        return render_template('register.html')


if __name__ == "__main__":
     try:
        client = MongoClient("mongodb://localhost:27017")
        db = client['PYTHON_MONGO_NCD_ID']
        Collection = db["PATIENT"]
        # client.server_info() #trigger exception if it cannot connect to database
        
     except Exception as e:
        print(e)
        print("Error - Cannot connect to database")
     app.run(debug=True)