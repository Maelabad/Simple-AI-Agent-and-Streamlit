from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from datetime import datetime

import logging

Base = declarative_base()

log = logging.getLogger(__name__)

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer(), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    url = Column(String(500), nullable=False)
    source = Column(String(100), nullable=False)
    date = Column(DateTime(), nullable=False)

    __table_args__ = (
        UniqueConstraint('url', name='unique_url'),
    )

    def __repr__(self):
        return f"<Dataset(title='{self.title}', source='{self.source}', date={self.date})>"


def init_db(db_url):
    """
    Initialise la base de données avec toutes les tables nécessaires
    
    Args:
        db_url: URL de connexion à la base de données
    Returns:
        engine: Le moteur SQLAlchemy créé
    """
    try:
        engine = create_engine(db_url)
        Base.metadata.create_all(engine) # Creation des tables
        log.info("Base de données initialisée avec succès")
        return engine
    except SQLAlchemyError as e:
        log.error(f"Erreur lors de l'initialisation de la base de données: {e}")
        raise

def insert(datasets, engine):
    
    try:
        # Création de la session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        for dataset in datasets:
            if isinstance(dataset['date'], str):
                dataset['date'] = datetime.strptime(dataset['date'], '%Y-%m-%d')
    
            result = Dataset(**dataset)
            session.add(result) # Insertion des données
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        log.error(f"Erreur lors de l'insertion des données : {e}")
    except Exception as e:
        session.rollback()
        log.error(f"Erreur inattendue : {e}")

    
    
    


