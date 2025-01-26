from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
import sklearn
# Create your views here.

# load ridge model from pickle file 
model = open('car.pkl', 'rb')
rg = pickle.load(model)

# load standard scaler from pickle file 
scale = open('car_scaler.pkl', 'rb')
sc = pickle.load(scale)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def attribute_input():
    if request.method == "POST":
        wheelbase = float(request.form.get("Wheel Base"))
        print(wheelbase)
        carlength  = float(request.form.get("Car lenght"))
        print(carlength)
        carwidth = float(request.form.get("Card Width"))
        curbweight = float(request.form.get("Curb wight"))
        cylindernumber = float(request.form.get("Cylinder Number"))
        enginesize = float(request.form.get("Engine Size"))
        boreratio = float(request.form.get("Bore ratio"))
        horsepower = float(request.form.get("Horse Power"))
        citympg = float(request.form.get("City Mpg"))
        highwaympg = float(request.form.get("HighWay Mpg"))
        stroke = float(request.form.get("Stroke"))
        peakrpm = float(request.form.get("Peak Rpm"))
        compressionratio = float(request.form.get("Compression Ratio"))
        fueltype = request.form.get("Fuel_Type")
        if (fueltype == "Gas"):
            fueltype_gas = 1
        else:
            fueltype_gas = 0

        enginetype = request.form.get("Engine type")

        if (enginetype == "DOHCV"):
            enginetype_dohcv = 1
            enginetype_l = 0
            enginetype_ohc = 0
            enginetype_ohcf = 0
            enginetype_ohcv = 0
            enginetype_rotor = 0

        elif (enginetype == "L"):
            enginetype_dohcv = 0
            enginetype_l = 1
            enginetype_ohc = 0
            enginetype_ohcf = 0
            enginetype_ohcv = 0
            enginetype_rotor = 0

        elif (enginetype == "OHC"):
            enginetype_dohcv = 0
            enginetype_l = 0
            enginetype_ohc = 1
            enginetype_ohcf = 0
            enginetype_ohcv = 0
            enginetype_rotor = 0

        elif (enginetype == "OHCF"):
            enginetype_dohcv = 0
            enginetype_l = 0
            enginetype_ohc = 0
            enginetype_ohcf = 1
            enginetype_ohcv = 0
            enginetype_rotor = 0

        elif (enginetype == "OHCV"):
            enginetype_dohcv = 0
            enginetype_l = 0
            enginetype_ohc = 0
            enginetype_ohcf = 0
            enginetype_ohcv = 1
            enginetype_rotor = 0

        elif (enginetype) == "ROTOR":
            enginetype_dohcv = 0
            enginetype_l = 0
            enginetype_ohc = 0
            enginetype_ohcf = 0
            enginetype_ohcv = 0
            enginetype_rotor = 1


        else:
            enginetype_dohcv = 0
            enginetype_l = 0
            enginetype_ohc = 0
            enginetype_ohcf = 0
            enginetype_ohcv = 0
            enginetype_rotor = 0

        carbody = request.form.get("Carbody")

        if (carbody == "Hardtop"):
            carbody_hardtop = 1
            carbody_hatchback = 0
            carbody_sedan = 0
            carbody_wagon = 0

        elif (carbody == "Hatchback"):
            carbody_hardtop = 0
            carbody_hatchback = 1
            carbody_sedan = 0
            carbody_wagon = 0

        elif (carbody == "Sedan"):
            carbody_hardtop = 0
            carbody_hatchback = 0
            carbody_sedan = 1
            carbody_wagon = 0

        elif (carbody == "Wagon"):
            carbody_hardtop = 0
            carbody_hatchback = 0
            carbody_sedan = 0
            carbody_wagon = 1

        else:
            carbody_hardtop = 0
            carbody_hatchback = 0
            carbody_sedan = 0
            carbody_wagon = 0

        fuelsystem = request.form.get("Fuel System")

        if (fuelsystem == "2BBL"):
            fuelsystem_2bbl = 1
            fuelsystem_4bbl = 0
            fuelsystem_idi = 0
            fuelsystem_mfi = 0
            fuelsystem_mpfi = 0
            fuelsystem_spdi = 0
            fuelsystem_spfi = 0

        elif (fuelsystem == "4BBL"):
            fuelsystem_2bbl = 0
            fuelsystem_4bbl = 1
            fuelsystem_idi = 0
            fuelsystem_mfi = 0
            fuelsystem_mpfi = 0
            fuelsystem_spdi = 0
            fuelsystem_spfi = 0

        elif (fuelsystem == "IDI"):
            fuelsystem_2bbl = 0
            fuelsystem_4bbl = 0
            fuelsystem_idi = 1
            fuelsystem_mfi = 0
            fuelsystem_mpfi = 0
            fuelsystem_spdi = 0
            fuelsystem_spfi = 0

        elif (fuelsystem == "MFI"):
            fuelsystem_2bbl = 0
            fuelsystem_4bbl = 0
            fuelsystem_idi = 0
            fuelsystem_mfi = 1
            fuelsystem_mpfi = 0
            fuelsystem_spdi = 0
            fuelsystem_spfi = 0

        elif (fuelsystem == "MPFI"):
            fuelsystem_2bbl = 0
            fuelsystem_4bbl = 0
            fuelsystem_idi = 0
            fuelsystem_mfi = 0
            fuelsystem_mpfi = 1
            fuelsystem_spdi = 0
            fuelsystem_spfi = 0

        elif (fuelsystem == "SPDI"):
            fuelsystem_2bbl = 0
            fuelsystem_4bbl = 0
            fuelsystem_idi = 0
            fuelsystem_mfi = 0
            fuelsystem_mpfi = 0
            fuelsystem_spdi = 1
            fuelsystem_spfi = 0

        elif fuelsystem == "SPFI":
            fuelsystem_2bbl = 0
            fuelsystem_4bbl = 0
            fuelsystem_idi = 0
            fuelsystem_mfi = 0
            fuelsystem_mpfi = 0
            fuelsystem_spdi = 0
            fuelsystem_spfi = 1


        else:
            fuelsystem_2bbl = 0
            fuelsystem_4bbl = 0
            fuelsystem_idi = 0
            fuelsystem_mfi = 0
            fuelsystem_mpfi = 0
            fuelsystem_spdi = 0
            fuelsystem_spfi = 0

        drivewheel = request.form.get("DriveWheel")
        if (drivewheel == "RWD"):
            drivewheel_rwd = 1
            drivewheel_fwd = 0

        elif (drivewheel == "FWD"):
            drivewheel_rwd = 0
            drivewheel_fwd = 1

        else:
            drivewheel_rwd = 0
            drivewheel_fwd = 0

        aspiration = request.form.get("Aspration")

        if (aspiration == "Turbo"):
            aspiration_turbo = 1
        else:
            aspiration_turbo = 0

        cylindernumber = request.form.get("Cylinder Number")

        array = [
            wheelbase, carlength, carwidth, curbweight, cylindernumber,
            enginesize, boreratio,stroke, compressionratio, horsepower,peakrpm,
            citympg, highwaympg,
            fueltype_gas, aspiration_turbo, carbody_hardtop,
            carbody_hatchback, carbody_sedan, carbody_wagon, drivewheel_fwd,
            drivewheel_rwd, enginetype_dohcv, enginetype_l, enginetype_ohc,
            enginetype_ohcf, enginetype_ohcv, enginetype_rotor,
            fuelsystem_2bbl, fuelsystem_4bbl, fuelsystem_idi,
            fuelsystem_mfi, fuelsystem_mpfi, fuelsystem_spdi,
            fuelsystem_spfi
        ]
        array = np.array(array)

        array = sc.transform([array])
        prediction = rg.predict(array)

        output = round(prediction[0], 2)
        return render_template('result.html', output=output)
    else:
        return render_template("home.html")
    

if __name__ == "__main__":
    app.run(debug=True)