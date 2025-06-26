
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
    try:
        cursor= mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_albums WHERE state= 1')
        consultaTodo= cursor.fetchall()
        return render_template('formulario.html', errores={},albums=consultaTodo)
    
    except Exception as e:
        print('Error al consultar todo: '+ str(e))
        return render_template('formulario.html', errores={},albums=[])
        
    finally:
        cursor.close()
        
        
#ruta de detalle
@app.route('/detalle/<int:id>')
def detalle(id):
    try:
        cursor= mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_albums WHERE id=%s',(id,))
        consultaId= cursor.fetchone()
        return render_template('consulta.html',album=consultaId)
    
    except Exception as e:
        print('Error al consultar por id : '+ str(e))
        return redirect(url_for('home'))
        
    finally:
        cursor.close()
        

#ruta para editar registro
@app.route('/editaAlbum/<int:id>')
def editar(id):
    try:
        cursor= mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_albums WHERE id=%s',(id,))
        consultaId= cursor.fetchone()
        return render_template('formUpdate.html',album=consultaId)
    
    except Exception as e:
        print('Error al consultar por id : '+str(e))
        return redirect(url_for('home'))
        
    finally:
        cursor.close()   


#ruta confirmar Delete
@app.route('/confirmaDel/<int:id>')
def confirma(id):
    try:
        cursor= mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_albums WHERE id=%s',(id,))
        consultaId= cursor.fetchone()
        return render_template('confirmDel.html',album=consultaId)
    
    except Exception as e:
        print('Error al consultar por id : '+str(e))
        return redirect(url_for('home'))
        
    finally:
        cursor.close()   
        
        
#ruta para el Actualizar
@app.route('/ActualizarAlbum/<int:id>',methods=['POST'])
def actualizar(id):
    
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
            cursor.execute('update tb_albums set album= %s, artista= %s, anio=%s where id= %s', (tituloV,artistaV,anioV, id))
            mysql.connection.commit()
            flash('Album Actulizado en BD')
            return redirect(url_for('home'))
        
        except Exception as e:
            mysql.connection.rollback()
            flash('Algo fallo: '+ str(e))
            return redirect(url_for('home'))
        
        finally: 
            cursor.close()
    
    return render_template('formulario.html',errores=errores)
       

#ruta para el Eliminar
@app.route('/EliminarAlbum/<int:id>',methods=['POST'])
def softDel(id):
    
    try:
        cursor= mysql.connection.cursor()
        cursor.execute('update tb_albums set state=%s where id= %s', (0, id))
        mysql.connection.commit()
        flash('Album Eliminado en BD')
        return redirect(url_for('home'))
        
    except Exception as e:
        mysql.connection.rollback()
        flash('Algo fallo: '+ str(e))
        return redirect(url_for('home'))
        
    finally: 
        cursor.close()



#ruta de para abrir detalle
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