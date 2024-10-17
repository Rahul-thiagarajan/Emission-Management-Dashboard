from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
import json
import matplotlib.pyplot as plt
import io,base64
import os
import werkzeug

customer=""
model=""
identity=""

path=r"C:/Users\\91934\\OneDrive\\Desktop\\Test\\"
app=Flask(__name__)

@app.route('/',methods=["GET"])
def display():
    return render_template("SelectCust.html")

@app.route("/testing",methods=["POST","GET"])
def test():
    try:
        if(request.form['back']=="back"):
            return redirect('/submit_customer')
    except werkzeug.exceptions.BadRequestKeyError:
        pass
    global path
    global customer
    global model
    global identity
    try:
        identity=request.form['identification']
    except werkzeug.exceptions.BadRequestKeyError:
        pass
    path= r"C:/Users\\91934\\OneDrive\\Desktop\\Test\\"
    path=path+customer+"\\"
    path=path+model+"\\"
    path=path+identity+"\\"
    try:
        x=request.form['report']
        if(x=="Entire Report"):
            files = []
            try:
                for filename in os.listdir(path):
                    if os.path.isfile(os.path.join(path, filename)):
                        files.append(filename)
            except FileNotFoundError:
                return "<body><h1>PARTICULAR FOLDER IS NOT AVAILABLE</h1><h1>CHECK THE NETWORK</h1><h1>RESTART THE APPLICATION</h1></body>"
            coValues=[]
            thcValues=[]
            noxValues=[]
            hcpnoxValues=[]
            co2Values=[]
            pmValues=[]
            for i in files:
                currentpath=path+i
                try:
                    data=pd.read_excel(currentpath,"Report")
                except PermissionError:
                    return "<body><h1>THE REQUESTED FILE IS OPEN</h1><h1>CLOSE THE FILE TO ACCESS IT</h1></body>"
                except FileNotFoundError:
                    return "<body><h1>FILE NOT FOUND</h1><h1>RESTART THE APPLICATION</h1></body>"
                fields=data.values.tolist()
                coValue=int(fields[10][1])
                thcValue=int(fields[10][3])
                noxValue=int(fields[10][5])
                hcpnoxValue=int(fields[10][6])
                co2Value=int(fields[10][7])
                pmValue=int(fields[10][8])
                coValues.append(coValue)
                thcValues.append(thcValue)
                noxValues.append(noxValue)
                hcpnoxValues.append(hcpnoxValue)
                co2Values.append(co2Value)
                pmValues.append(pmValue)
            categories = ['CO\nmin','CO\nmax', 'THC\nmin','THC\nmax', 'NOx\nmin','NOx\nmax', 'HC+NOx\nmin','HC+NOx\nmax', 'CO2\nmin','CO2\nmax','PM\nmin','PM\nmax']
            values=[min(coValues),max(coValues),min(thcValues),max(thcValues),min(noxValues),max(noxValues),min(hcpnoxValues),max(hcpnoxValues),min(co2Values),max(co2Values),min(pmValues),max(pmValues)]
            plt.figure(figsize=(10, 6))
            cmap = plt.get_cmap('viridis')
            colors = [cmap(i / len(values)) for i in range(len(values))]
            plt.bar(categories, values, color=colors)
            for i, value in enumerate(values):
                plt.text(i, value + 0.5, str(value), ha='center', va='bottom')
            plt.title(f'EMISSION VALUES REPORT OF {customer}')
            plt.xlabel('Components')
            plt.ylabel('Values (mg/km)')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = 'data:image/png;base64,' + string.decode('utf-8')
            return render_template('Report.html',url=uri)
    except werkzeug.exceptions.BadRequestKeyError:
        pass
    files = []
    print(path)
    try:
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                files.append(filename)
        #print(files)
    except FileNotFoundError:
        return "<body><h1>PARTICULAR FOLDER IS NOT AVAILABLE</h1><h1>CHECK THE NETWORK</h1><h1>RESTART THE APPLICATION</h1></body>"
    return render_template("SelectFile.html",selectedcustomer=customer,selectedmodel=model,selectediden=identity,dataValues=files)

@app.route('/submit_customer',methods=["POST","GET"])
def submit_customer():
    global customer
    try:
        customer=request.form['customer']
    except werkzeug.exceptions.BadRequestKeyError:
        pass
    global path
    path=r"C:/Users\\91934\\OneDrive\\Desktop\\Test\\"
    path=path+customer+"\\"
    print(path)
    listOfModels=[]
    try:
        for filename in os.listdir(path):
            if not os.path.isfile(os.path.join(path, filename)):
                listOfModels.append(filename)
    except FileNotFoundError:
        return "<body><h1>PARTICULAR FOLDER IS NOT AVAILABLE</h1><h1>CHECK THE NETWORK</h1><h1>RESTART THE APPLICATION</h1></body>"
    return render_template("SelectModel.html",selectedcustomer=customer,models=listOfModels)

@app.route('/submit_model',methods=["POST","GET"])
def submit_model():
    try:
        if(request.form['back']=="back"):
            return redirect('/')
    except werkzeug.exceptions.BadRequestKeyError:
        pass
    global model
    try:
        model=request.form['vehicle_model']
    except werkzeug.exceptions.BadRequestKeyError:
        pass
    global path
    global customer
    path=r"C:/Users\\91934\\OneDrive\\Desktop\\Test\\"
    path=path+customer+"\\"
    path=path+model+"\\"
    print(path)
    listOfIdentification=[]
    try:
        for filename in os.listdir(path):
            if not os.path.isfile(os.path.join(path, filename)):
                listOfIdentification.append(filename)
    except FileNotFoundError:
        return "<body><h1>PARTICULAR FOLDER IS NOT AVAILABLE</h1><h1>CHECK THE NETWORK</h1><h1>RESTART THE APPLICATION</h1></body>"
    return render_template('SelectIden.html',selectedcustomer=customer,selectedmodel=model,identificationList=listOfIdentification)

@app.route('/display_graph',methods=["POST","GET"])
def showGraph():
    try:
        if(request.form['back']=="back"):
            return redirect('/submit_model')
    except werkzeug.exceptions.BadRequestKeyError:
        pass
    filename = request.form['fileName']
    choice = request.form['choice']
    global path
    currentpath = path + filename
    print(currentpath)
    try:
        limits=pd.read_excel("application.xlsx","Sheet1")
        data=pd.read_excel(currentpath,"Report")
        data1 = pd.read_excel(currentpath, "Continuous")
        data2 = pd.read_excel(currentpath, "ContinuousResults")
    except PermissionError:
        return "<body><h1>THE REQUESTED FILE IS OPEN</h1><h1>CLOSE THE FILE TO ACCESS IT</h1></body>"
    limitValues=limits.values.tolist()
    fields=data.values.tolist()
    testNo=fields[0][7]
    regulationCycle=fields[1][7]
    vehicleClass=fields[2][4]
    vehicleModel=fields[3][4]
    customer=fields[5][4]
    coValue=int(fields[10][1])
    thcValue=int(fields[10][3])
    noxValue=int(fields[10][5])
    hcpnoxValue=int(fields[10][6])
    co2Value=int(fields[10][7])
    pmValue=int(fields[10][8])
    Inertia=int(fields[52][0])
    graphUrls=[]
    displayDetails=[customer,vehicleClass,vehicleModel,regulationCycle]
    tallPM=0
    tallNOX=0
    tallCO=0
    tallHCPNOX=0

    v1PM=0
    v1NOX=0
    v1CO=0
    v1HCPNOX=0

    obd2PM=0
    obd2NOX=0
    obd2CO=0
    obd2HC=0

    obd2elPM=0
    obd2elNOX=0
    obd2elCO=0
    obd2elHC=0
    for i in range(1,len(limitValues)):
        print(vehicleClass,limitValues[i][1],vehicleClass in limitValues[i][1])
        if(limitValues[i][0]==Inertia and vehicleClass in limitValues[i][1]):
            tallPM=limitValues[i][6]
            tallNOX=limitValues[i][4]
            tallCO=limitValues[i][3]
            tallHCPNOX=limitValues[i][5]

            v1PM=limitValues[i][10]
            v1NOX=limitValues[i][8]
            v1CO=limitValues[i][7]
            v1HCPNOX=limitValues[i][9]

            obd2PM=limitValues[i][14]
            obd2NOX=limitValues[i][13]
            obd2CO=limitValues[i][11]
            obd2HC=limitValues[i][12]

            obd2elPM=limitValues[i][18]
            obd2elNOX=limitValues[i][17]
            obd2elCO=limitValues[i][15]
            obd2elHC=limitValues[i][16]

    g1x1=0
    g1x2=0
    g1y1=0
    g1y2=0
    g1px=0
    g1py=0

    g2x1=0
    g2x2=0
    g2y1=0
    g2y2=0
    g2px=0
    g2py=0

    g3x1=0
    g3x2=0
    g3y1=0
    g3y2=0
    g3px=0
    g3py=0
    
    if(choice == "tpl"):
        g1x1=tallNOX
        g1x2=v1NOX
        g1y1=tallPM
        g1y2=v1PM
        g1px=noxValue
        g1py=pmValue

        g2x1=tallHCPNOX
        g2x2=v1HCPNOX
        g2y1=tallPM
        g2y2=v1PM
        g2px=hcpnoxValue
        g2py=pmValue

        g3x1=tallHCPNOX
        g3x2=v1HCPNOX
        g3y1=tallCO
        g3y2=v1CO
        g3px=hcpnoxValue
        g3py=coValue
    else:
        g1x1=obd2NOX
        g1x2=obd2elNOX
        g1y1=obd2PM
        g1y2=obd2elPM
        g1px=noxValue
        g1py=pmValue

        g2x1=obd2HC
        g2x2=obd2elHC
        g2y1=obd2PM
        g2y2=obd2elPM
        g2px=thcValue
        g2py=pmValue

        g3x1=obd2HC
        g3x2=obd2elHC
        g3y1=obd2CO
        g3y2=obd2elCO
        g3px=thcValue
        g3py=coValue
    opacityValues = data1["Opacity"].tolist()
    noxgsValues = data2["DiluteNOXRate"].tolist()
    noxppmValues = data2["DiluteNOXCorrConc"].tolist()
    thcgsValues = data2["DiluteTHCRate"].tolist()
    thcppmValues = data2["DiluteTHCCorrConc"].tolist()
    speedValues = data1["SpeedFeedback"].tolist()
    COppmValues = data2["DiluteCOCorrConc"].tolist()
    timeValues = data2["LogTime"].tolist()
    cogsValues= data2["DiluteCORate"].tolist()
    opacityValues =  [float(i) for i in opacityValues[1:]]
    timeValues = [float(i) for i in timeValues[1:]]
    speedValues = [float(i) for i in speedValues[1:]]
    COppmValues = [float(i) for i in COppmValues[1:]]
    cogsValues = [float(i) for i in cogsValues[1:]]
    thcppmValues = [float(i) for i in thcppmValues[1:]]
    thcgsValues = [float(i) for i in thcgsValues[1:]]
    noxppmValues = [float(i) for i in noxppmValues[1:]]
    noxgsValues = [float(i) for i in noxgsValues[1:]]
    # Plot 1 pm vs nox
    plt.figure(figsize=(10, 6))
    plt.plot([0, g1x1, g1x1, 0, 0], [0, 0, g1y1, g1y1, 0], color='green', alpha=0.6, linewidth=2)
    plt.plot([0, g1x2, g1x2, 0, 0], [0, 0, g1y2, g1y2, 0], color='Slateblue', alpha=0.6, linewidth=2)
    plt.scatter(g1px, g1py, color='red', s=100, label='Point')
    plt.title('PM vs NOX')
    plt.xlim(0, max(g1x1,g1x2)+1)
    plt.ylim(0, max(g1y1,g1y2) + 1)
    plt.xlabel('NOX')
    plt.ylabel('PM')
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    string1 = base64.b64encode(buf1.read())
    uri1 = 'data:image/png;base64,' + string1.decode('utf-8')
    graphUrls.append(uri1)
    plt.close()

    # Plot 9 pm vs hc+nox
    plt.figure(figsize=(10, 6))
    plt.plot([0, g2x1, g2x1, 0, 0], [0, 0, g2y1, g2y1, 0], color='green', alpha=0.6, linewidth=2)
    plt.plot([0, g2x2, g2x2, 0, 0], [0, 0, g2y2, g2y2, 0], color='Slateblue', alpha=0.6, linewidth=2)
    plt.scatter(g2px, g2py, color='red', s=100, label='Point')
    plt.title('PM vs NOX')
    plt.xlim(0, max(g2x1,g2x2)+1)
    plt.ylim(0, max(g2y1,g2y2) + 1)
    plt.xlabel('HC+NOX')
    plt.ylabel('PM')
    buf9 = io.BytesIO()
    plt.savefig(buf9, format='png')
    buf9.seek(0)
    string9 = base64.b64encode(buf9.read())
    uri9 = 'data:image/png;base64,' + string9.decode('utf-8')
    graphUrls.append(uri9)
    plt.close()

    # Plot 10 co vs thc
    plt.figure(figsize=(10, 6))
    plt.plot([0, g3x1, g3x1, 0, 0], [0, 0, g3y1, g3y1, 0], color='green', alpha=0.6, linewidth=2)
    plt.plot([0, g3x2, g3x2, 0, 0], [0, 0, g3y2, g3y2, 0], color='Slateblue', alpha=0.6, linewidth=2)
    plt.scatter(g3px, g3py, color='red', s=100, label='Point')
    plt.title('PM vs NOX')
    plt.xlim(0, max(g3x1,g3x2)+1)
    plt.ylim(0, max(g3y1,g3y2) + 1)
    plt.xlabel('CO')
    plt.ylabel('THC')
    buf10 = io.BytesIO()
    plt.savefig(buf10, format='png')
    buf10.seek(0)
    string10 = base64.b64encode(buf10.read())
    uri10 = 'data:image/png;base64,' + string10.decode('utf-8')
    graphUrls.append(uri10)
    plt.close()

    # Plot 2 co ppm
    plt.figure(figsize=(10, 6))
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = 'tab:red'
    ax1.set_xlabel('Time Values')
    ax1.set_ylabel('Speed', color=color)
    ax1.scatter(timeValues, speedValues, color=color, label='Speed', s=2)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('CO ppm', color=color)
    ax2.scatter(timeValues, COppmValues, color=color, label='CO ppm', s=2)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()  
    plt.title('Scatter Plot with Two Y Values')
    plt.grid()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    string2 = base64.b64encode(buf2.read())
    uri2 = 'data:image/png;base64,' + string2.decode('utf-8')
    graphUrls.append(uri2)
    plt.close()

    # Plot 3 co gs
    plt.figure(figsize=(10, 6))
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = 'tab:red'
    ax1.set_xlabel('Time Values')
    ax1.set_ylabel('Speed', color=color)
    ax1.scatter(timeValues, speedValues, color=color, label='Speed', s=2)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('CO g/s', color=color)
    ax2.scatter(timeValues, cogsValues, color=color, label='CO g/s', s=2)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()  
    plt.title('Scatter Plot with Two Y Values')
    plt.grid()
    buf3 = io.BytesIO()
    plt.savefig(buf3, format='png')
    buf3.seek(0)
    string3 = base64.b64encode(buf3.read())
    uri3 = 'data:image/png;base64,' + string3.decode('utf-8')
    graphUrls.append(uri3)
    plt.close()

    # Plot 4 thc ppm
    plt.figure(figsize=(10, 6))
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = 'tab:red'
    ax1.set_xlabel('Time Values')
    ax1.set_ylabel('Speed', color=color)
    ax1.scatter(timeValues, speedValues, color=color, label='Speed', s=2)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('THC ppm', color=color)
    ax2.scatter(timeValues, thcppmValues, color=color, label='THC ppm', s=2)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout() 
    plt.title('Scatter Plot with Two Y Values')
    plt.grid()
    buf4 = io.BytesIO()
    plt.savefig(buf4, format='png')
    buf4.seek(0)
    string4 = base64.b64encode(buf4.read())
    uri4 = 'data:image/png;base64,' + string4.decode('utf-8')
    graphUrls.append(uri4)
    plt.close()

    # Plot 5 thc gs
    plt.figure(figsize=(10, 6))
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = 'tab:red'
    ax1.set_xlabel('Time Values')
    ax1.set_ylabel('Speed', color=color)
    ax1.scatter(timeValues, speedValues, color=color, label='Speed', s=2)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('THC gs', color=color)
    ax2.scatter(timeValues, thcgsValues, color=color, label='THC gs', s=2)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout() 
    plt.title('Scatter Plot with Two Y Values')
    plt.grid()
    buf5 = io.BytesIO()
    plt.savefig(buf5, format='png')
    buf5.seek(0)
    string5 = base64.b64encode(buf5.read())
    uri5 = 'data:image/png;base64,' + string5.decode('utf-8')
    graphUrls.append(uri5)
    plt.close()

    # Plot 6 nox ppm
    plt.figure(figsize=(10, 6))
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = 'tab:red'
    ax1.set_xlabel('Time Values')
    ax1.set_ylabel('Speed', color=color)
    ax1.scatter(timeValues, speedValues, color=color, label='Speed', s=2)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('NOX ppm', color=color)
    ax2.scatter(timeValues, noxppmValues, color=color, label='NOX ppm', s=2)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout() 
    plt.title('Scatter Plot with Two Y Values')
    plt.grid()
    buf6 = io.BytesIO()
    plt.savefig(buf6, format='png')
    buf6.seek(0)
    string6 = base64.b64encode(buf6.read())
    uri6 = 'data:image/png;base64,' + string6.decode('utf-8')
    graphUrls.append(uri6)
    plt.close()

    # Plot 7 nox gs
    plt.figure(figsize=(10, 6))
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = 'tab:red'
    ax1.set_xlabel('Time Values')
    ax1.set_ylabel('Speed', color=color)
    ax1.scatter(timeValues, speedValues, color=color, label='Speed', s=2)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('NOX gs', color=color)
    ax2.scatter(timeValues, noxgsValues, color=color, label='NOX gs', s=2)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout() 
    plt.title('Scatter Plot with Two Y Values')
    plt.grid()
    buf7 = io.BytesIO()
    plt.savefig(buf7, format='png')
    buf7.seek(0)
    string7 = base64.b64encode(buf7.read())
    uri7 = 'data:image/png;base64,' + string7.decode('utf-8')
    graphUrls.append(uri7)
    plt.close()

    # Plot 8 opacity
    plt.figure(figsize=(10, 6))
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = 'tab:red'
    ax1.set_xlabel('Time Values')
    ax1.set_ylabel('Speed', color=color)
    ax1.scatter(timeValues, speedValues, color=color, label='Speed', s=2)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Opacity', color=color)
    ax2.scatter(timeValues, opacityValues, color=color, label='Opacity', s=2)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout() 
    plt.title('Scatter Plot with Two Y Values')
    plt.grid()
    buf8 = io.BytesIO()
    plt.savefig(buf8, format='png')
    buf8.seek(0)
    string8 = base64.b64encode(buf8.read())
    uri8 = 'data:image/png;base64,' + string8.decode ('utf-8')
    graphUrls.append(uri8)
    plt.close()
    return render_template("Main.html",details=displayDetails,gUrls=graphUrls)

if(__name__=='__main__'):
    app.run(debug="True")