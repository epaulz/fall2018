from flask import *
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import time

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'SECRET'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'aisner'
app.config['MYSQL_DATABASE_PASSWORD'] = 'WattTeam6'
app.config['MYSQL_DATABASE_DB'] = 'DriverIncentiveDB'
app.config['MYSQL_DATABASE_HOST'] = 'mysql1.cs.clemson.edu'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        # Read posted values from UI (underscore before variable name usually denotes a private variable)
        #_name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Validate received values
        if _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', ( _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                session['user'] = data[0][0]
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/showSignIn')
def showSignIn():
    if session.get('user'):
        try:
            if session.get('user'):
                _user = session.get('user')
                _perm = 1

                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_getInfo',(_user,_perm))
                user_info = cursor.fetchall()

                userInfo_dict = []
                for info in user_info:
                    info_dict = {
                        'ID': info[0],
                        'Username': info[1],
                        'Name': info[2],
                        'Address': info[3],
                        'Phone Number': info[4]
                    }
                    userInfo_dict.append(info_dict)

                cursor.callproc('sp_getPhoto',(_user,))
                photo_info = cursor.fetchall()
                #print(photo_info[0][0])
                
                cursor.callproc('sp_getPoints',(_user,))
                points = cursor.fetchall()
                
                points_list = []
                for elem in points:
                    points_list.append([elem[1],elem[0]])

                name = userInfo_dict[0]['Name']
                del userInfo_dict[0]['Name']

                #return json.dumps(info_dict)
                return render_template('userHome.html', data=[str(photo_info[0][0]),userInfo_dict,name,points_list])
            else:
                return render_template('error.html', error = 'Unauthorized Access')
        except Exception as e:
            return render_template('error.html', error = str(e))
    else:
        return render_template('signIn.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mySql
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][2]),'admin'):
                session['admin'] = data[0][0]
                return redirect('/admin')
            elif str(data[0][5]) == '1':
                return render_template('error.html',error = 'The Account is no longer active')
            elif check_password_hash(str(data[0][2]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password OR The Account is no longer active.')

    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/updateProfSettings', methods=['POST'])
def updateProfSettings():
    try:
        _name = request.form['inputName']
        _address = request.form['inputAddress']
        _phone = request.form['inputPhone']
        _url = request.form['inputURL']


        if session.get('user'):
            _user = session.get('user')

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_updateName',(_user,_name))
            cursor.callproc('sp_updateAddress',(_user,_address))
            cursor.callproc('sp_updatePhone',(_user,_phone))
            cursor.callproc('sp_updatePhoto',(_user,_url))
            con.commit()

            return redirect('/profSettings')

        else:
            return render_template('error.html', error = 'An Error Occurred')
    except Exception as e:
        return render_template('error.html', error = str(e))

    finally:
            cursor.close()
            con.close()

''' OLD USER HOME
@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('index.html')
'''

@app.route('/userHome')
def userHome():
    if session.get('user'):
        try:
            if session.get('user'):
                _user = session.get('user')
                _perm = 1

                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_getInfo',(_user,_perm))
                user_info = cursor.fetchall()

                userInfo_dict = []
                for info in user_info:
                    info_dict = {
                        'ID': info[0],
                        'Username': info[1],
                        'Name': info[2],
                        'Address': info[3],
                        'Phone Number': info[4]
                    }
                    userInfo_dict.append(info_dict)

                cursor.callproc('sp_getPhoto',(_user,))
                photo_info = cursor.fetchall()
                #print(photo_info[0][0])
                
                cursor.callproc('sp_getPoints',(_user,))
                points = cursor.fetchall()
                
                points_list = []
                for elem in points:
                    points_list.append([elem[1],elem[0]])

                name = userInfo_dict[0]['Name']
                del userInfo_dict[0]['Name']

                #return json.dumps(info_dict)
                return render_template('userHome.html', data=[str(photo_info[0][0]),userInfo_dict,name,points_list])
            else:
                return render_template('error.html', error = 'Unauthorized Access')
        except Exception as e:
            return render_template('error.html', error = str(e))

    else:
        return render_template('index.html')

@app.route('/profSettings')
def profSettings():
    if session.get('user') or session.get('admin'):
        return render_template('profileSettings.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@app.route('/profHistory')
def profHistory():
    if session.get('user'):
        try:
            if session.get('user'):
                _user = session.get('user')
                _perm = 1

                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_getPurchases',(_user,))
                x = cursor.fetchall()
                x = x[::-1]
                
                headers = ['ID','Timestamp','Points Spent']

                return render_template('profileHistory.html', data=[headers,x])
            else:
                return render_template('error.html', error = 'Unauthorized Access')

        except Exception as e:
            return render_template('error.html', error = str(e))

    else:
        return render_template('index.html')

@app.route('/adminSettings')
def adminSettings():
    if session.get('admin'):
        return render_template('adminSettings.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@app.route('/sponsorSettings')
def sponsorSettings():
    if session.get('sponsor'):
        return render_template('sponsorSettings.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')        

@app.route('/updatedprofSettings')
def updatedprofSettings():
    if session.get('user') or session.get('admin'):
        return render_template('updatedprofilesettings.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@app.route('/regConfirm')
def regConfirm():
    return render_template('registrationConfirmation.html')

@app.route('/aboutContact')
def aboutContact():
    return render_template('aboutUsWithContact.html')

@app.route('/catProd')
def catProd():
    if session.get('user') or session.get('admin') or session.get('sponsor'):
        return render_template('catalogProductPage.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@app.route('/catOrdRevSub')
def catOrdRevSub():
    if session.get('user') or session.get('admin'):
        return render_template('catalogOrderReviewSubmit.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@app.route('/catOrdConf')
def catOrdConf():
    if session.get('user') or session.get('admin'):
        return render_template('catalogOrderConfirmation.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@app.route('/catListView')
def catListView():
    if session.get('user') or session.get('admin'):
        return render_template('catalogItemListView.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@app.route('/catHome')
def catHome():
    if session.get('user') or session.get('admin') or session.get('sponsor'):
        return render_template('catalogHome.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@app.route('/catProduct')
def catProduct():
    if session.get('user'):
        return render_template('catalogProductPage.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@app.route('/dynamiccatView')
def dynamiccatView():
    if session.get('user'):
        return render_template('dynamicCatalogView.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')


@app.route('/dynamiccatProduct')
def dynamiccatProduct():
    if session.get('user'):
        return render_template('dynamicProductPage.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')


@app.route('/submit')
def submit():
    return render_template('submitpage.html')

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUsWithContact.html')

@app.route('/reactivate')
def reactivate():
    return render_template('reactivation.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('admin', None)
    session.pop('sponsor', None)
    return render_template('index.html')

@app.route('/showResetPass')
def showResetPass():
    return render_template('resetPassword.html')

@app.route('/resetPass', methods=['POST'])
def resetPass():
    try:
        _email = request.form['inputEmail']
        _oldPassword = request.form['inputPassword']
        _newPassword = request.form['inputNewPassword']

        if _email and _oldPassword and _newPassword:
            con = mysql.connect()
            cursor = con.cursor()
            _hashed_password = generate_password_hash(_newPassword)
            cursor.callproc('sp_resetPassword',(_email, _hashed_password,))
            data = cursor.fetchall()

            if len(data) == 0:
                con.commit()
                return render_template('error.html', error = 'Reset Password Successful')
            else:
                return render_template('error.html', error = 'Wrong Email or Password')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/deleteAcct', methods=['POST'])
def deleteAcct():
    try:
        _email = request.form['inputEmail']
        _Password = request.form['inputPassword']

        if _email and _Password:
            con = mysql.connect()
            cursor = con.cursor()
            _hashed_password = generate_password_hash(_Password)
            cursor.callproc('sp_deleteAcct',(_email, _hashed_password))
            data = cursor.fetchall()

            if len(data) == 0:
                con.commit()
                return render_template('error.html', error = 'Account Deleted.')
            else:
                return render_template('error.html', error = 'Wrong Email or Password')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/admin')
def admin():
    if session.get('admin'):
        return render_template('adminHome.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access! You must be an admin to view this page!')

@app.route('/getInfo')
def getInfo():
    try:
        if session.get('user'):
            _user = session.get('user')
            _perm = 1

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_getInfo',(_user,_perm))
            user_info = cursor.fetchall()

            userInfo_dict = []
            for info in user_info:
                info_dict = {
                    'ID': info[0],
                    'Username': info[1],
                    'Address': info[2],
                    'Phone Number': info[3]
                }
                userInfo_dict.append(info_dict)
            return json.dumps(info_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/showSponsorReg')
def showSponsorReg():
    return render_template('sponsorReg.html')

@app.route('/sponsorReg', methods=['GET','POST'])
def sponsorReg():
    try:
        # Read posted values from UI (underscore before variable name usually denotes a private variable)
        _name = request.form['inputName']
        _password = request.form['inputPassword']

        # Validate received values
        if _name and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createSponsor', ( _name, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                json.dumps({'message':'User created successfully !'})
                return render_template("registrationConfirmation.html")
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/sponsorHome')
def sponsorHome():
    if (session.get('sponsor')):
        try:
            if session.get('sponsor'):
                _sponsorID = session.get('sponsor')
                _perm = 2

                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_getInfo',(_sponsorID,_perm))
                user_info = cursor.fetchall()

                user_info_list = user_info[0]

                company_name = user_info_list[1]

                sponsor_info_dict = {}
                sponsor_info_dict['Company Account ID'] = user_info_list[0]
                sponsor_info_dict['Point Weight'] = user_info_list[2]

                cursor.callproc('sp_getDrivers',(_sponsorID,))
                drivers = cursor.fetchall()

                return render_template('sponsorHome.html', data=[company_name,sponsor_info_dict,drivers])
            else:
                return render_template('error.html', error = 'Unauthorized Access')
        except Exception as e:
            return render_template('error.html', error = str(e))
    else:
        return render_template('index.html')

@app.route('/showSponsorSI')
def showSponsorSI():
    if (session.get('sponsor')):
        try:
            if session.get('sponsor'):
                _sponsorID = session.get('sponsor')
                _perm = 2

                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_getInfo',(_sponsorID,_perm))
                user_info = cursor.fetchall()

                user_info_list = user_info[0]

                company_name = user_info_list[1]

                sponsor_info_dict = {}
                sponsor_info_dict['Company Account ID'] = user_info_list[0]
                sponsor_info_dict['Point Weight'] = user_info_list[2]

                cursor.callproc('sp_getDrivers',(_sponsorID,))
                drivers = cursor.fetchall()

                return render_template('sponsorHome.html', data=[company_name,sponsor_info_dict,drivers])
            else:
                return render_template('error.html', error = 'Unauthorized Access')
        except Exception as e:
            return render_template('error.html', error = str(e))
    else:
        return render_template('sponsorLogIn.html')

@app.route('/sponsorLogIn',methods=['POST'])
def sponsorLogIn():
    try:
        _name = request.form['inputName']
        _password = request.form['inputPassword']

        # connect to mySql
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateSponsorLogin',(_name,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][6]),_password):
                session['sponsor'] = data[0][0]
                #return render_template('sponsorHome.html')
                return sponsorHome()
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/showAdminReg')
def showadminReg():
    return render_template('adminReg.html')

@app.route('/adminReg', methods=['GET','POST'])
def adminReg():
    try:
        # Read posted values from UI (underscore before variable name usually denotes a private variable)
        _name = request.form['inputName']
        _password = request.form['inputPassword']

        # Validate received values
        if _name and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createAdmin', ( _name, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                json.dumps({'message':'Admin created successfully !'})
                return render_template("registrationConfirmation.html")
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/adminHome')
def adminHome():
    if (session.get('admin')):
        try:
            if session.get('admin'):
                _adminID = session.get('admin')
                _perm = 3

                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_getInfo',(_adminID,_perm))
                user_info = cursor.fetchall()

                user_info_list = user_info[0]

                admin_name = user_info_list[1]

                admin_info_dict = {}
                admin_info_dict['Admin ID'] = user_info_list[0]

                cursor.callproc('sp_getAllDrivers',())
                drivers = cursor.fetchall()

                return render_template('adminHome.html', data=[admin_name,drivers])
            else:
                return render_template('error.html', error = 'Unauthorized Access')
        except Exception as e:
            return render_template('error.html', error = str(e))
    else:
        return render_template('index.html')

@app.route('/showAdminSI')
def showAdminSI():
    if (session.get('admin')):
        try:
            if session.get('admin'):
                _adminID = session.get('admin')
                _perm = 3

                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_getInfo',(_adminID,_perm))
                user_info = cursor.fetchall()

                user_info_list = user_info[0]

                admin_name = user_info_list[1]

                admin_info_dict = {}
                admin_info_dict['Admin ID'] = user_info_list[0]

                cursor.callproc('sp_getAllDrivers',())
                drivers = cursor.fetchall()

                return render_template('adminHome.html', data=[admin_name,drivers])
            else:
                return render_template('error.html', error = 'Unauthorized Access')
        except Exception as e:
            return render_template('error.html', error = str(e))
    else:
        return render_template('adminLogIn.html')

@app.route('/adminLogIn',methods=['POST'])
def adminLogIn():
    try:
        _name = request.form['inputName']
        _password = request.form['inputPassword']

        # connect to mySql
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateAdminLogin',(_name,))
        data = cursor.fetchall()

        if len(data) > 0:
            session['admin'] = data[0][0]
                #return render_template('adminHome.html')
            return adminHome()
        else:
            return render_template('error.html',error = 'Wrong Username or Password.')

    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/test')
def test_route():
    try:
        if session.get('user'):
            _user = session.get('user')
            _perm = 1

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_getInfo',(_user,_perm))
            user_info = cursor.fetchall()

            userInfo_dict = []
            for info in user_info:
                info_dict = {
                    'ID': info[0],
                    'Username': info[1],
                    'Address': info[2],
                    'Phone Number': info[3]
                }
                userInfo_dict.append(info_dict)
            
            #return json.dumps(info_dict)
            return render_template('userHome.html', data=userInfo_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/checkout')
def checkout():
    _user = session.get('user')
    points_cost = 1

    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('sp_purchase', (_user,points_cost))
    con.commit()
    cursor.fetchall()

    cursor.callproc('sp_purchPoints', (_user,points_cost*-1))
    con.commit()
    cursor.fetchall()

    purchaseTime=time.time()
    cancelTime = time.time() + (60*60*48)

    return render_template('checkoutConfirm.html')
  
purchaseTime=time.time()
cancelTime = purchaseTime + (60*60*48)

@app.route('/cancel')
def cancel():
    if (time.time() <= cancelTime):
        return render_template('cancelConfirm.html')
    else:
        return render_template('error.html', error = "It has been more than 2 days after the purchase date. You can not cancel")

@app.route('/addEmployee', methods=['POST'])
def addEmployee():
    try:
        # Read posted values from UI (underscore before variable name usually denotes a private variable)
        _DName = request.form['inputDriver']
        _SName = request.form['inputCompany']

        # Validate received values
        if _DName and _SName:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addEmploy', (_DName, _SName))
            conn.commit()
            
            return redirect('/sponsorSettings')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/dropEmployee', methods=['POST'])
def dropEmployee():
    try:
        # Read posted values from UI (underscore before variable name usually denotes a private variable)
        _DName = request.form['inputDriver']
        _SName = request.form['inputCompany']

        # Validate received values
        if _DName and _SName:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_remEmploy', (_DName, _SName))
            conn.commit()
            
            return redirect('/sponsorSettings')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/updatePoints', methods=['POST'])
def updatePoints():
    try:
        _DName = request.form['inputDriver']
        _SName = request.form['inputCompany']
        _Points = request.form['inputPoints']

        if _DName and _Points:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updatePoints', (_DName, _SName, _Points))
            conn.commit()

            return redirect('/sponsorSettings')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/updatePW', methods=['POST'])
def updatePW():
    try:
        _SName = request.form['inputName']
        _PW = request.form['inputPW']

        if _SName and _PW:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updatePtVal', (_SName, _PW))
            conn.commit()

            return redirect('/sponsorSettings')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)

