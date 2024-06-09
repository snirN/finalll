from sqlalchemy import  Column , ForeignKey ,Integer, String ,Float,DateTime
import datetime
from database import base
from sqlalchemy.orm import Relationship

import passlib.hash as _hash


class Organizations(base):
    __tablename__ = "organizations"

    organization_id = Column(Integer,primary_key=True , index=True,autoincrement=True)
    organization_name = Column(String(80),nullable=False)
    bucket = Column(Float,nullable=False)
    bucketLeft = Column(Float,nullable=False)

    deletevolumerequests =  Relationship("DeleteVolumeRequests",back_populates="organization",passive_deletes=True)
    users = Relationship("Users",back_populates="organization",passive_deletes=True)
    volumes = Relationship("Volumes",back_populates="organization",passive_deletes=True)

   



    
class Users(base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True , index=True,autoincrement=True)
    email = Column(String(80),nullable=False,unique=True)
    hash_password = Column(String(80),nullable=False)
    organization_id = Column(Integer,ForeignKey("organizations.organization_id",ondelete="CASCADE"),nullable=True)
    role = Column(Integer,ForeignKey("roles.role_id"),nullable=False)

    def verify_password(self, password: str):
            return _hash.bcrypt.verify(password, self.hash_password)

    bucketrequests = Relationship("BucketRequests",back_populates="users",passive_deletes=True)
    deletevolumerequests = Relationship("DeleteVolumeRequests",back_populates="users",passive_deletes=True)   
    organization = Relationship("Organizations",back_populates="users")
    role1 = Relationship("Roles",back_populates="users")
   

    



class Volumes(base):
    __tablename__ = "volumes"
    volume_id = Column(Integer,primary_key=True ,autoincrement=True)
    volume_name = Column(String(80),nullable=False)
    volume_real_id = Column(String(80),nullable=False)
    organization_id = Column(Integer,ForeignKey("organizations.organization_id",ondelete="CASCADE"),nullable=False)
    size = Column(Float,nullable=False)

    organization = Relationship("Organizations",back_populates="volumes")
    deletevolumerequests = Relationship("DeleteVolumeRequests",back_populates="volumes",passive_deletes=True)   
 


class BucketRequests(base):
    __tablename__ = "bucketrequests"
    
    request_id = Column(Integer,primary_key=True  ,autoincrement=True)
    request_date = Column(DateTime,default=datetime.datetime.utcnow,nullable=False)
    architect_id = Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)
    size =  Column(Float,nullable=False)
    details = Column(String(80),nullable=True,default=" ")
    status_id = Column(Integer,ForeignKey("status.status_id"),default=1,nullable=False)


    users = Relationship("Users", back_populates="bucketrequests")
    status = Relationship("Status",back_populates="bucketrequests")



   
class DeleteVolumeRequests(base):
    __tablename__ = "deletevolumerequests"
    
    request_id = Column(Integer,primary_key=True  ,autoincrement=True)
    request_date = Column(DateTime,default=datetime.datetime.utcnow,nullable=False)
    user_id = Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)
    organization_id = Column(Integer,ForeignKey("organizations.organization_id",ondelete="CASCADE"),nullable=False)
    volume_id = Column(Integer,ForeignKey("volumes.volume_id",ondelete="CASCADE"),nullable=False)
    details = Column(String(80),nullable=True,default=" ")
    status_id = Column(Integer,ForeignKey("status.status_id"),default=1,nullable=False) 
  
    organization = Relationship("Organizations", back_populates="deletevolumerequests")
    users = Relationship("Users", back_populates="deletevolumerequests")
    volumes = Relationship("Volumes", back_populates="deletevolumerequests")
    status = Relationship("Status",back_populates="deletevolumerequests")



class Status(base):
    __tablename__ = "status"

    status_id = Column(Integer,primary_key=True ,autoincrement=True)
    status_name = Column(String(80),nullable=False)

    bucketrequests = Relationship("BucketRequests",back_populates="status",passive_deletes=True) 
    deletevolumerequests = Relationship("DeleteVolumeRequests",back_populates="status",passive_deletes=True)   
     



class Roles(base):
    __tablename__ = "roles"

    role_id = Column(Integer,primary_key=True ,autoincrement=True)
    roles_name = Column(String(80),nullable=False)
    
    
    users = Relationship("Users",back_populates="role1",passive_deletes=True)    


