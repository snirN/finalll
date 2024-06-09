import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import sqlalchemy.orm as _orm
from sqlalchemy import desc
import passlib.hash as _hash
import database as database , models as models , schemas as schemas ,ontapServices
import os
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET") #salt
oauth2schema = _security.OAuth2PasswordBearer(tokenUrl=os.getenv("tokenUrl")) #protocol that checks the jwt token in a safe way

# Dependency
def get_db():
    db = database.sessionlocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_role(user: schemas.Users, db: _orm.Session):
  user = db.query(models.Users).filter(models.Users.user_id == user.user_id).first()  
  return user.role 

async def create_organization(manager: schemas.Users,organization: schemas.OrganizationsCreate, db: _orm.Session):
    organization_obj = models.Organizations(
        organization_name = organization.organization_name,
        bucket = organization.bucket,
        bucketLeft = organization.bucket
    )
    if manager.role==1:
        db.add(organization_obj)
        db.commit()
        db.refresh(organization_obj)
        return organization_obj

    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized"
        )



async def create_architect(manager: schemas.Users,organization:schemas.Organizations,architect: schemas.UsersCreate, db: _orm.Session):
    user_obj = models.Users(
        email=architect.email, hash_password=_hash.bcrypt.hash(architect.hash_password)
        ,organization_id=organization.organization_id,role=2
    )
    if manager.role==1:
    
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj
    
    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")


async def organization_selector(organization_id: int, db: _orm.Session):
    organization = (
        db.query(models.Organizations)
        .filter(models.Organizations.organization_id == organization_id)
        .first()
    )
    
    if organization is None:
        raise _fastapi.HTTPException(status_code=404, detail="organization does not exist")

    return organization



async def get_organizations(user: schemas.Users, db: _orm.Session):
    organizations = db.query(models.Organizations)
    if user.role == 1:
        return list(map(schemas.Organizations.from_orm, organizations))

    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")



async def delete_organization(manager: schemas.Users,organization_id: int, db: _orm.Session):
    volumes =  (
        db.query(models.Volumes)
        .filter(models.Volumes.organization_id == organization_id)
        .all()
    )
    if manager.role==1:
        for volume in volumes:
            ontapServices.delete(volume.volume_real_id)
            db.delete(volume)
            db.commit()


        organization = await organization_selector(organization_id, db)
        db.delete(organization)
        db.commit()

    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")


#if there's a user it will return him else return null
async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(models.Users).filter(models.Users.email == email).first()   




async def get_users_per_organization(user: schemas.Users, db: _orm.Session):
        users = db.query(models.Users).filter(models.Users.organization_id==user.organization_id)
        if user.role == 2:
            return list(map(schemas.Users.from_orm, users))
        else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")

    
#create user and encrypt the password with bcrypt
async def create_user(architect: schemas.Users,user: schemas.UsersCreate, db: _orm.Session):
    user_obj = models.Users(
        email=user.email, hash_password=_hash.bcrypt.hash(user.hash_password)
        ,organization_id=architect.organization_id,role=3
    )
    if architect.role==2:
    
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj
    
    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized"
        )




async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db =db, email =email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: models.Users):
    user_obj = schemas.Users.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET) #give the token the payload and salt for creating

    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.Users).get(payload["user_id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return schemas.Users.from_orm(user)



async def user_selector(user_id: int, db: _orm.Session):
    user = (
        db.query(models.Users)
        .filter(models.Users.user_id == user_id)
        .first()
    )
    
    if user is None:
        raise _fastapi.HTTPException(status_code=404, detail="user does not exist")

    return user

async def delete_user(user_id: int,arcitect: schemas.Users ,db: _orm.Session):
    if arcitect.role == 2:
        if user_id != arcitect.user_id:
            user = await user_selector(user_id, db)
            if arcitect.organization_id == user.organization_id:
                db.delete(user)
                db.commit()
        else:
         raise _fastapi.HTTPException(
            status_code=401, detail="cant delete yourself"
        )        
    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized"
        )





async def create_requestForIncreaseBucket(user: schemas.Users,request: schemas.BucketRequestsCreate, db: _orm.Session):
    request_obj = models.BucketRequests(
       architect_id =  user.user_id,size = request.size,details=request.details,status_id = 1
    )

    if user.role == 2:
        db.add(request_obj)
        db.commit()
        db.refresh(request_obj)
    return request_obj



async def bucketRequest_selector(request_id: int, db: _orm.Session):
    request = (
        db.query(models.BucketRequests)
        .filter(models.BucketRequests.request_id == request_id)
        .first()
    )

    if request is None:
        raise _fastapi.HTTPException(status_code=404, detail="request does not exist")

    return request



async def get_bucketRequests(user: schemas.Users, db: _orm.Session):
    bucketRequests = db.query(models.BucketRequests).order_by(desc(models.BucketRequests.request_date))
    if user.role == 1:
        return list(map(schemas.BucketRequests.from_orm, bucketRequests))

    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")


async def get_organization_by_user_id(user_id: int, db: _orm.Session):
    return db.query(models.Organizations).filter(models.Organizations.organization_id ==
    models.Users.organization_id).filter(models.Users.user_id == user_id).first()


async def update_Bucket_Approved(request_id: int,manager: schemas.Users, db: _orm.Session):
    if manager.role == 1 :
            
        request = await bucketRequest_selector(request_id,db)
        if request.status_id == 1:

            organization =  await get_organization_by_user_id(request.architect_id,db)
            organization.bucket = organization.bucket+ request.size
            organization.bucketLeft = organization.bucketLeft+ request.size

            db.commit()
            db.refresh(organization)

            request.status_id = 2
            db.commit()
            db.refresh(request)

        
        
        else:
         raise _fastapi.HTTPException(
            status_code=406, detail="already updated")


    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")

async def update_Bucket_Denied(request_id: int,manager: schemas.Users, db: _orm.Session):
    if manager.role == 1 :
        request = await bucketRequest_selector(request_id,db)
        if request.status_id == 1:
                request.status_id = 3

                db.commit()
                db.refresh(request)
                return request
    

        else:
         raise _fastapi.HTTPException(
            status_code=406, detail="already updated")    
    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")






async def get_bucket(user: schemas.Users, db: _orm.Session):
    organization = db.query(models.Organizations).filter(models.Organizations.organization_id == user.organization_id).first()   
    organization_bucket = organization.bucket
    return organization_bucket


async def get_bucketLeft(user: schemas.Users, db: _orm.Session):
    organization = db.query(models.Organizations).filter(models.Organizations.organization_id == user.organization_id).first()   
    organization_bucketLeft = organization.bucketLeft
    return organization_bucketLeft





async def get_volumes_per_organization(user: schemas.Users, db: _orm.Session):
        volumes = db.query(models.Volumes).filter(models.Volumes.organization_id==user.organization_id).order_by(models.Volumes.volume_id)
        return list(map(schemas.Volumes.from_orm, volumes))

   

async def get_volume_by_name(volume_name: str, db: _orm.Session):
    return db.query(models.Volumes).filter(models.Volumes.volume_name == volume_name).first()   



async def create_volume(volume: schemas.VolumesCreate,user: schemas.Users, db: _orm.Session):
    if volume.size<20:
        raise _fastapi.HTTPException(
            status_code=401, detail="need more then 20")

     
    if volume.volume_name.isalpha() == False:
         raise _fastapi.HTTPException(
            status_code=401, detail="name with only letters")


    if volume.volume_name ==  get_volume_by_name(volume.volume_name, db):
        raise _fastapi.HTTPException(
            status_code=401, detail="other name")

    organization = await organization_selector(user.organization_id,db)
    if volume.size < organization.bucketLeft:
        volume_uuid = ontapServices.create(volume.volume_name,volume.size)

        volume_obj = models.Volumes(
        volume_name = volume.volume_name,size = volume.size, organization_id = organization.organization_id,
          volume_real_id=volume_uuid)
        
        db.add(volume_obj)
        db.commit()
        db.refresh(volume_obj)

        organization.bucketLeft = organization.bucketLeft - volume.size
        db.commit()
        db.refresh(organization)

        return volume_obj

    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not enough space in bucket")





async def volume_selector(volume_id: int, user: schemas.Users, db: _orm.Session):
    volume = (
        db.query(models.Volumes)
        .filter(models.Volumes.organization_id == user.organization_id)
        .filter(models.Volumes.volume_id == volume_id)
        .first()
    )

    if volume is None:
        raise _fastapi.HTTPException(status_code=404, detail="volume does not exist")

    return volume



async def get_volume(volume_id: int, user: schemas.Users, db: _orm.Session):
    volume = await volume_selector(volume_id,user,db)

    return volume


async def get_volume2(volume_id: int, user: schemas.Users, db: _orm.Session):
    volume = await volume_selector(volume_id,user,db)

    return schemas.Volumes.from_orm(volume)


async def volumeSizeIncrease(size:float,volume_id:int,user:schemas.Users, db: _orm.Session):
    organization = await organization_selector(user.organization_id,db)
    volume = await volume_selector(volume_id,user,db)

    if size>19:
        if size<organization.bucketLeft:
                if size>volume.size:
                    difference = size - volume.size
                    volume.size = size
                    ontapServices.update(volume.volume_real_id,volume.size)
                    db.commit()
                    db.refresh(volume)
                    organization.bucketLeft = organization.bucketLeft - difference
                    db.commit()
                    db.refresh(organization)
                else:
                    raise _fastapi.HTTPException(status_code=400, detail="not increased")    

        else:
            raise _fastapi.HTTPException(status_code=400, detail="not enough space in bucket")


    else:
        raise _fastapi.HTTPException(status_code=400, detail="need to be greater than 20 mb")
          


async def volumeSizeDecrease(size:float,volume_id:int,user:schemas.Users, db: _orm.Session):
    organization = await organization_selector(user.organization_id,db)
    volume = await volume_selector(volume_id,user,db)

    if size>19:
        if size<volume.size:
                difference = volume.size - size 
                volume.size = size
                ontapServices.update(volume.volume_real_id,volume.size)
                db.commit()
                db.refresh(volume)
                organization.bucketLeft = organization.bucketLeft + difference
                db.commit()
                db.refresh(organization)

        else:
            raise _fastapi.HTTPException(status_code=400, detail="not decreased")         

    else:
        raise _fastapi.HTTPException(status_code=400, detail="need to be greater than 20 mb")



        
async def create_requestForDeleteVolume(user: schemas.Users,request: schemas.DeleteVolumeRequestsCreate, db: _orm.Session):
    
    request_obj = models.DeleteVolumeRequests(
       user_id =  user.user_id,organization_id=user.organization_id,volume_id =request.volume_id,details=request.details,status_id = 1
    )
    requestBefore = (db.query(models.DeleteVolumeRequests) #if already requested
        .filter(models.DeleteVolumeRequests.volume_id == request_obj.volume_id)
        .first())
    if requestBefore:
        request2 = await DeleteVolumeRequest_selector(requestBefore.request_id, db)
        if  request2.status_id!=3:
            raise _fastapi.HTTPException(status_code=400, detail="request already exist")
    
    volume = db.query(models.Volumes).filter(models.Volumes.volume_id==request.volume_id).first()
    if user.organization_id == volume.organization_id:         #if the request is from someone from the right organization
        db.add(request_obj)
        db.commit()
        db.refresh(request_obj)
        return request_obj



async def DeleteVolumeRequest_selector(request_id: int, db: _orm.Session):
    request = (
        db.query(models.DeleteVolumeRequests)
        .filter(models.DeleteVolumeRequests.request_id == request_id)
        .first()
    )

    if request is None:
        raise _fastapi.HTTPException(status_code=404, detail="request does not exist")

    return request



async def get_DeleteVolumeRequests(architect: schemas.Users, db: _orm.Session):

    DeleteVolumeRequests = db.query(models.DeleteVolumeRequests).filter(models.DeleteVolumeRequests.organization_id == architect.organization_id).order_by(models.DeleteVolumeRequests.request_date)
    if architect.role == 2:
        return list(map(schemas.DeleteVolumeRequests.from_orm, DeleteVolumeRequests))

    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")




async def DeleteVolume_Approved(request_id: int,architect: schemas.Users, db: _orm.Session):
    if architect.role == 2 :
            
        request = await DeleteVolumeRequest_selector(request_id,db)
        volume = await get_volume(request.volume_id,architect,db)
        if request.status_id == 1:
            
            ontapServices.delete(volume.volume_real_id)
            organization =  await get_organization_by_user_id(request.user_id,db)
            organization.bucketLeft = organization.bucketLeft + volume.size
            
            db.commit()
            db.refresh(organization)
             
            db.delete(volume)
            db.commit()


        
        else:
         raise _fastapi.HTTPException( 
            status_code=406, detail="already updated")


    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")

async def DeleteVolume_Denied(request_id: int,architect: schemas.Users, db: _orm.Session):
    if architect.role == 2 :
        request = await DeleteVolumeRequest_selector(request_id,db)
        if request.status_id == 1:
                request.status_id = 3

                db.commit()
                db.refresh(request)
                return request
    

        else:
         raise _fastapi.HTTPException(
            status_code=406, detail="already updated")    
    else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")


async def get_all_volumes(user: schemas.Users, db: _orm.Session):
        if user.role == 1 :
            volumes = db.query(models.Volumes).order_by(models.Volumes.organization_id)
            return list(map(schemas.Volumes.from_orm, volumes))

        else:
         raise _fastapi.HTTPException(
            status_code=401, detail="not authurized")
        


async def recFunc(user: schemas.Users,volume_id:int, db: _orm.Session):
            volume = await get_volume(volume_id,user,db)
            data = ontapServices.recFunc(volume.volume_real_id)
            return data
      