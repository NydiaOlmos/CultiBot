import csv
from models import *
from datetime import datetime
from sqlalchemy import select

def carga_datos_prueba(db):
    try:
        # ------------- PLANTAS ----------------
        with open('DatosPrueba/plantas.csv', mode='r', encoding='utf-8') as file_plantas:
            # Extrae las filas de plantas
            reader_plantas = csv.DictReader(file_plantas)
            
            for row in reader_plantas:
                # Modela una nueva planta
                nueva_planta = Planta(
                    nombre=row['nombre'],
                    tipo=row['tipo'],
                    tipo_suelo=Suelo(row['tipo_suelo'])
                )

                # Añade la planta a la consulta
                db.add(nueva_planta)
        
        # Commit para guardar todas las plantas en la db
        db.commit()

        print("Plantas cargadas")

        # ------------- MÉTRICAS --------------
        with open('DatosPrueba/metricas.csv', mode='r', encoding='utf-8') as file_metrica:
            # Extrae las métricas de las plantas
            reader_metricas = csv.DictReader(file_metrica)

            for row in reader_metricas:
                # Verificamos que la planta exista
                query = select(Planta).where(Planta.id_planta == int(row['id_planta']))
                planta = db.scalar(query)

                if planta:
                    # Modela una nueva métrica
                    nueva_metrica = Metrica(
                        id_planta = int(row['id_planta']),
                        humedad_suelo = float(row['humedad_suelo']),
                        temperatura_ambiente = float(row['temperatura_ambiente']),
                        luminosidad = float(row['luminosidad']),
                        nitrogeno = float(row['nitrogeno']),
                        potasio = float(row['potasio']),
                        fosforo = float(row['fosforo']),
                        fecha = datetime.strptime(row['fecha'], "%Y-%m-%d %H:%M:%S")
                    )

                    # Añade la métrica a la consulta
                    db.add(nueva_metrica)
                else:
                    print(f"No se encontro la planta con el ID {row['id_planta']}")

            # Commit de la consulta
            db.commit()

            print("Métricas cargadas")

    except Exception as e:
        db.rollback() # Si ocurre algún error, se deshacen los cambios no commiteados
        print(f"Error durante el proceso: {e}")
        return False
    finally:
        db.close()
    return True