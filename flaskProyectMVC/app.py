
from flask import Flask,jsonify
from flask_mysqldb import MySQL
import MySQLdb

app= Flask(__name__)
mysql= MySQL(app)

 

#RUTAS DE GESTION INTERNA

#ruta try-Catch
@app.errorhandler(404)
def paginaNoE(e):
    return 'Cuidado: Error de capa 8 !!!',404

@app.errorhandler(405)
def metodonoP(e):
    return 'Revisa el metodo de envio de tu ruta (GET o POST) !!!',405 

#ruta para probar la conexion a MYSQL
@app.route('/DBCheck')
def DB_check():
    try:
        cursor= mysql.connection.cursor()
        cursor.execute('Select 1')
        return jsonify( {'status':'ok','message':'Conectado con exito'} ),200   
    except MySQLdb.MySQLError as e:
        return jsonify( {'status':'error','message':str(e)} ),500




if __name__ == '__main__':
    app.run(port=3000,debug=True)