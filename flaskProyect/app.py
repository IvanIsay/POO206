
from flask import Flask,jsonify
from flask_mysqldb import MySQL
import MySQLdb

app= Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="dbFlask"
#app.config['MYSQL_PORT']=3306 //Usar solo en cambio de puerto

mysql= MySQL(app)

#ruta para probar la conexion a MYSQL
@app.route('/DBCheck')
def DB_check():
    try:
        cursor= mysql.connection.cursor()
        cursor.execute('Select 1')
        return jsonify( {'status':'ok','message':'Conectado con exito'} ),200   
    except MySQLdb.MySQLError as e:
        return jsonify( {'status':'error','message':str(e)} ),500


#ruta simple
@app.route('/')
def home():
    return 'Hola Mundo FLASK'

#ruta con parametros
@app.route('/saludo/<nombre>')
def saludar(nombre):
    return 'Hola,'+nombre+'!!!'

#ruta try-Catch
@app.errorhandler(404)
def paginaNoE(e):
    return 'Cuidado: Error de capa 8 !!!',404

@app.errorhandler(405)
def metodonoP(e):
    return 'Revisa el metodo de envio de tu ruta (GET o POST) !!!',405 

#ruta doble
@app.route('/usuario')
@app.route('/usuaria')
def dobleroute():
    return 'Soy el mismo recurso del servidor'

#ruta POST
@app.route('/formulario',methods=['POST'])
def formulario():
    return 'Soy un formulario'



if __name__ == '__main__':
    app.run(port=3000,debug=True)