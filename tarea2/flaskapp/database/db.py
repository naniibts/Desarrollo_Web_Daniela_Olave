from sqlalchemy import create_engine, Column, Integer, DateTime, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# --- Clases ---
class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

class Comuna(Base):
    __tablename__ = 'comuna'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

class AvisoAdopción(Base):
    __tablename__ = 'aviso_adopcion'

    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15))
    tipo_mascota = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_edad = Column(String(10), nullable=False)
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(Text)

class ContactarPor(Base):
    __tablename__ = 'contactar_por'

    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'), primary_key=True)
    red_social = Column(String(50), nullable=False)

class FotoAviso(Base):
    __tablename__ = 'foto_aviso'

    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'), primary_key=True)
    ruta_foto = Column(String(255), primary_key=True)

#--- Funciones de acceso a datos ---

# Obtener las comunas por región
def get_regiones_y_comunas():
    session = SessionLocal()
    try:
        regiones = session.query(Region).all()
        resultado = []
        for r in regiones:
            comunas = session.query(Comuna).filter_by(region_id=r.id).all()
            resultado.append({
                "id": r.id,
                "nombre": r.nombre,
                "comunas": [{"id": c.id, "nombre": c.nombre} for c in comunas]
            })
        return resultado
    finally:
        session.close()

# Validar la existencia de la comuna en la bd (asi se evita inyección o bypass)
def existencia_comuna(comuna_id):
    session = SessionLocal()
    try:
        comuna = session.query(Comuna).filter_by(id=comuna_id).first()
        return comuna is not None
    finally:
        session.close()

# Agregar un nuevo aviso de adopción
def agregar_aviso(comuna_id, sector, nombre, email, celular,
                   tipo_mascota, cantidad, edad, unidad_edad, 
                   fecha_entrega, descripcion):
    
    session = SessionLocal()
    try:
        nuevo_aviso = AvisoAdopción(
            comuna_id=comuna_id,
            sector=sector,
            nombre=nombre,
            email=email,
            celular=celular,
            tipo_mascota=tipo_mascota,
            cantidad=cantidad,
            edad=edad,
            unidad_edad=unidad_edad,
            fecha_entrega=fecha_entrega,
            descripcion=descripcion
        )
        session.add(nuevo_aviso)
        session.commit()
        return nuevo_aviso.id
    finally:
        session.close()

# Agregar las redes de contacto para un aviso
def agregar_redes_contacto(aviso_id, redes):
    session = SessionLocal()
    try:
        contacto = ContactarPor(aviso_id=aviso_id, red_social=redes)
        session.add(contacto)            
        session.commit()
    finally:
        session.close()

# Agregar las fotos para un aviso
def agregar_fotos(aviso_id, ruta_foto):
    session = SessionLocal()
    try:
        foto = FotoAviso(aviso_id=aviso_id, ruta_foto=ruta_foto)
        session.add(foto)            
        session.commit()
    finally:
        session.close()

# Obtener los últimos 5 avisos de adopción
def get_last_avisos(limit=5):
    session = SessionLocal()
    try:
        return session.query(AvisoAdopción).order_by(AvisoAdopción.id.desc()).limit(limit).all()
        
    finally:
        session.close()

# Contar los avisos para la paginación
def contar_avisos():
    session = SessionLocal()
    try:
        return session.query(AvisoAdopción).count()
    finally:
        session.close()

# Listar avisos con paginación
def listar_avisos(offset=0, limit=5):
    session = SessionLocal()
    try:
        return session.query(AvisoAdopción).order_by(AvisoAdopción.id.desc()).offset(offset).limit(limit).all()
    finally:
        session.close()

# Obtener un aviso por su ID con fotos y contactos
def get_aviso_por_id(aviso_id):
    session = SessionLocal()
    try:
        aviso = session.query(AvisoAdopción).filter_by(id=aviso_id).first()
        if aviso:
            session.query(FotoAviso).filter_by(aviso_id=aviso_id).all()
            session.query(ContactarPor).filter_by(aviso_id=aviso_id).all()
        return aviso
        
    finally:
        session.close()