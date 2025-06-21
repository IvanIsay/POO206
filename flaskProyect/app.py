
from flask import Flask,jsonify,render_template,request,url_for,flash,redirect
from flask_mysqldb import MySQL
import MySQLdb

app= Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="dbFlask"
#app.config['MYSQL_PORT']=3306 //Usar solo en cambio de puerto
app.secret_key='mysecretkey'

mysql= MySQL(app)


#ruta de inicio
@app.route('/')
def home():
    return render_template('formulario.html', errores={})

#ruta de conusta
@app.route('/consulta')
def consulta():
    return render_template('consulta.html')

#ruta para el Insert
@app.route('/guardarAlbum',methods=['POST'])
def guardar():
    
    #lista de errores
    errores={}
    
    #obtener los datos a insertar
    tituloV= request.form.get('txtTitulo','').strip()
    artistaV= request.form.get('txtArtista','').strip()
    anioV= request.form.get('txtAnio','').strip()
    
    if not tituloV:
        errores['txtTitulo']= 'Nombre del album Obligatorio'
    if not artistaV:
        errores['txtArtista']= 'Artista es Obligatorio'
    if not anioV:
        errores['txtAnio']= 'Año es Obligatorio'
    elif not anioV.isdigit() or int(anioV)< 1800 or int(anioV) > 2100 :
        errores['txtAnio']= 'Ingresa una año Valido'       
        
    if not errores:
        try:
            cursor= mysql.connection.cursor()
            cursor.execute('insert into tb_albums(album,artista,anio) values(%s,%s,%s)',(tituloV,artistaV,anioV) )
            mysql.connection.commit()
            flash('Album guardado en BD')
            return redirect(url_for('home'))
        
        except Exception as e:
            mysql.connection.rollback()
            flash('Algo fallo: '+ str(e))
            return redirect(url_for('home'))
        
        finally: 
            cursor.close()
    
    return render_template('formulario.html',errores=errores)










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