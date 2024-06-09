import database as database , models as models 
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import os
from dotenv import load_dotenv

load_dotenv()





database.base.metadata.create_all(bind=database.engine)

def create_organizations(db: _orm.Session):
    organization = models.Organizations(organization_name='manager',bucket=10000,bucketLeft=10000)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    organization = models.Organizations(organization_name='google',bucket=1000,bucketLeft=1000)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    organization = models.Organizations(organization_name='mamram',bucket=1000,bucketLeft=1000)
    db.add(organization)
    db.commit()
    db.refresh(organization)




def create_roles(db: _orm.Session):
    role = models.Roles(roles_name='manager')
    db.add(role)
    db.commit()
    db.refresh(role)
    role = models.Roles(roles_name='architect')
    db.add(role)
    db.commit()
    db.refresh(role)
    role = models.Roles(roles_name='worker')
    db.add(role)
    db.commit()
    db.refresh(role)
   
def create_statuses(db: _orm.Session):
    status = models.Status(status_name='in progres')
    db.add(status)
    db.commit()
    db.refresh(status)
    status = models.Status(status_name='confirmed')
    db.add(status)
    db.commit()
    db.refresh(status)
    status = models.Status(status_name='denied')
    db.add(status)
    db.commit()
    db.refresh(status)
 
 
      
def create_manager(db: _orm.Session):
    manager = models.Users(email=os.getenv("managerEmail"),hash_password=_hash.bcrypt.hash(os.getenv("managerPassword")),organization_id=1,role=1)
    db.add(manager)
    db.commit()
    db.refresh(manager)
   
   
     
def create_architects(db: _orm.Session):
    architect = models.Users(email=os.getenv("arichtect1Email"),hash_password=_hash.bcrypt.hash(os.getenv("arichtect1Password")),organization_id=2,role=2)
    db.add(architect)
    db.commit()
    db.refresh(architect)
    architect = models.Users(email=os.getenv("arichtect2Email"),hash_password=_hash.bcrypt.hash(os.getenv("arichtect2Password")),organization_id=3,role=2)
    db.add(architect)
    db.commit()
    db.refresh(architect)
    db.close()


db = database.sessionlocal()
create_organizations(db)
create_roles(db)
create_statuses(db)
create_manager(db)
create_architects(db)