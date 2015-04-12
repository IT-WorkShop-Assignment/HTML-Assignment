from flask import Flask,request,render_template,make_response
import numpy.polynomial.polynomial as P
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import re

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def Home():
    return render_template('home.html',value='COMPUTER ASSIGNMENT',title='Home')

@app.route('/biodata')
def Biodata():
    return render_template('biodata.html',value='Biodata',title='Biodata')

@app.route('/biodata/aman')
def Aman():
    return render_template('aman.html',value='Aman Gupta',title='Aman')

@app.route('/biodata/amit')
def Amit():
    return render_template('amit.html',value='Amit Kumar',title='Amit')

@app.route('/biodata/murari')
def Murari():
    return render_template('murari.html',value='Murari',title='Murari')

@app.route('/average',methods=['GET','POST'])
def Average():


    if request.method=='GET':
        return render_template('average.html',value='Average',title='Average',result="")
    elif request.method=='POST':
        first = request.form['first']
        temp=first

        s=first[:]+','
        first=[]
        while(s!=''):
            i=s.index(',')
            first.append(float(s[:i]))
            s=s[i+1:]

        sum=0
        for item in first:
            sum=sum+item
            rest=float(sum)/len(first)






        return render_template('average2.html',value='Average',title='Average',result=rest,oldvalue=temp)
    else:

        return 'Invalid Request'

@app.route('/interpolation',methods=['GET','POST'])
def Interpolation():
    if request.method=='GET':
        return render_template('interpolation.html',value='Interpolation',title='Interpolation')

    elif request.method=='POST':
        points=request.form['points']
        return render_template('interpolation2.html',value='Interpolation',title='Interpolation',source='/plot/'+points,old_points=points)

    else:
        return 'Invalid Request'

@app.route('/plot/<points>')
def plot(points):
    s,X,F=points[:],[],[]
    while(s!=''):
        i=s.index('(')
        j=s.index(',',i)
        X.append(float(s[i+1:j]))
        k=s.index(')',j)
        F.append(float(s[j+1:k]))
        s=s[k+2:]
    fig=plt.figure()
    plt.clf()
    sub=fig.add_subplot(111)
    X1=np.arange(min(X)-2,max(X)+2,0.1)
    num_plots=len(X)
    #colormap = plt.cm.gist_ncar
  #  plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0.2, 0.9, num_plots)])
    x=[1.0]
    for i in range(len(X)):
        x=P.polymul(x,[-1*X[i],1])
    b=[0.0]
    for i in range(len(X)):
        a=P.polydiv(x,[-1*X[i],1])
        b=P.polyadd(P.polymul((P.polydiv(a[0],P.polyval(X[i],a[0])))[0],[F[i]]),b)
        Y=P.polyval(X1,P.polymul((P.polydiv(a[0],P.polyval(X[i],a[0])))[0],[F[i]]))
        sub.plot(X1,Y)

    Y=P.polyval(X1,b)
    Y1=P.polyval(np.arange(min(X),max(X)+0.1,0.1),b)
    interpol_obj=sub.plot(X1,Y,'k',linewidth=2)
    #sub.fill_between( X1, Y ,alpha=0.5)
    sub.plot(X,F,'ro',markersize=6)

    plt.grid(True)
    fig.legend(interpol_obj,['Interpolation'],fancybox=True,shadow=True,loc='upper left')
    plt.axis([min(X)-3,max(X)+3,min(Y1)-2,max(Y1)+2])
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.title('Interpolation')

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())


    return response

if __name__ == '__main__':
    app.run(debug=True)
