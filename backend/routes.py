from typing import List
import fastapi.security as _security
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as services , schemas as schemas 


app = _fastapi.FastAPI()



@app.get("/api/get_user_role",tags=["Get"])
async def get_user_role(
    user: schemas.Users = _fastapi.Depends(services.get_current_user),
    db: _orm.Session = _fastapi.Depends(services.get_db),
):
    return await services.get_user_role(user, db)


@app.post("/api/create_organization",tags=["Post"])
async def create_organization(
     architect: schemas.UsersCreate,
     organization: schemas.OrganizationsCreate,
     db: _orm.Session = _fastapi.Depends(services.get_db),
     manager:schemas.Users=_fastapi.Depends(services.get_current_user),
     
    
):
 db_user = await services.get_user_by_email(architect.email, db)
 if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

 organization = await services.create_organization(manager,organization, db)
 await services.create_architect(manager,organization,architect,db)
 



@app.get("/api/get_organizations", response_model=List[schemas.Organizations],tags=["Get"])
async def get_organizations(
    user: schemas.Users = _fastapi.Depends(services.get_current_user),
    db: _orm.Session = _fastapi.Depends(services.get_db),
):
    return await services.get_organizations(user=user, db=db)




@app.delete("/api/organizations/{organization_id}", status_code=204 ,tags=["Delete"])
async def delete_organization(
    organization_id: int,
    db: _orm.Session = _fastapi.Depends(services.get_db),
    manager:schemas.Users=_fastapi.Depends(services.get_current_user),
):
    await services.delete_organization( manager,organization_id, db)
    return {"message", "Successfully Deleted"}


@app.get("/api/get_users_per_organization", response_model= List[schemas.Users],tags=["Get"])
async def get_users_per_organization(user: schemas.Users = _fastapi.Depends(services.get_current_user),
                          db: _orm.Session = _fastapi.Depends(services.get_db),):
    return await services.get_users_per_organization(user,db)

@app.post("/api/users",tags=["Post"])
async def create_user(
    user: schemas.UsersCreate,
    architect:schemas.Users=_fastapi.Depends(services.get_current_user), 
    db: _orm.Session = _fastapi.Depends(services.get_db),
    
):
       
       db_user = await services.get_user_by_email(user.email, db)
       if db_user:
            raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

       user = await services.create_user(architect,user, db)


@app.post("/api/token",tags=["Post"])
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(services.get_db),
):
    user = await services.authenticate_user(form_data.username, form_data.password, db) 

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await services.create_token(user)

@app.get("/api/users/me", response_model=schemas.Users,tags=["Get"])
async def get_user(user: schemas.Users = _fastapi.Depends(services.get_current_user)):
    return user



@app.delete("/api/users/{user_id}", status_code=204,tags=["Delete"])
async def delete_user(
    user_id: int ,
    architect: schemas.Users = _fastapi.Depends(services.get_current_user),
    db: _orm.Session = _fastapi.Depends(services.get_db),
):
    await services.delete_user(user_id, architect, db)
    return {"message", "Successfully Deleted"}




@app.post("/api/create_volume",tags=["Post"])
async def create_volume(
        volume: schemas.VolumesCreate,
        user:schemas.Users=_fastapi.Depends(services.get_current_user),
        db: _orm.Session = _fastapi.Depends(services.get_db),

    
):
        volume = await services.create_volume(volume,user, db)




@app.post("/api/create_request_For_Increase_Bucket",tags=["Post"])
async def create_request_For_Increase_Bucket(
    request: schemas.BucketRequestsCreate,
    user:schemas.Users=_fastapi.Depends(services.get_current_user),
    db: _orm.Session = _fastapi.Depends(services.get_db),
    
):
    request = await services.create_requestForIncreaseBucket(user,request,db)
    return {"message", "Successfully created"}

@app.put("/api/update_Bucket_Approved/{request_id}",tags=["Put"])
async def update_Bucket_Approved(request_id: int,
                        manager: schemas.Users = _fastapi.Depends(services.get_current_user),
                        db: _orm.Session = _fastapi.Depends(services.get_db),
    
):
        request = await services.update_Bucket_Approved(request_id,manager,db)
        return {"message", "Successfully updated"}                          


@app.put("/api/update_Bucket_Denied/{request_id}",tags=["Put"])
async def update_Bucket_Denied(request_id: int,
                        manager: schemas.Users = _fastapi.Depends(services.get_current_user),
                        db: _orm.Session = _fastapi.Depends(services.get_db),
    
):
        request = await services.update_Bucket_Denied(request_id,manager,db)  
        return {"message", " updated denied"}        



@app.put("/api/volumeSizeIncrease/{volume_id}/{size}",tags=["Put"])
async def volumeSizeIncrease(
        size:float,
        volume_id:int,
        user: schemas.Users = _fastapi.Depends(services.get_current_user),
        db: _orm.Session = _fastapi.Depends(services.get_db),
    
):
        await services.volumeSizeIncrease(size,volume_id,user, db)  




@app.put("/api/volumeSizeDecrease/{volume_id}/{size}",tags=["Put"])
async def volumeSizeDecrease(
        size:float,
        volume_id:int,
        user: schemas.Users = _fastapi.Depends(services.get_current_user),
        db: _orm.Session = _fastapi.Depends(services.get_db),
    

    
):
        await services.volumeSizeDecrease(size,volume_id,user, db)                



@app.get("/api/bucketRequests", response_model=List[schemas.BucketRequests],tags=["Get"])
async def get_bucket_Requests(
    user: schemas.Users = _fastapi.Depends(services.get_current_user),
    db: _orm.Session = _fastapi.Depends(services.get_db),
):
    return await services.get_bucketRequests(user=user, db=db)



@app.get("/api/get_bucket", response_model= float,tags=["Get"])
async def get_bucket(user: schemas.Users = _fastapi.Depends(services.get_current_user),
                     db: _orm.Session = _fastapi.Depends(services.get_db),):
    return await services.get_bucket(user,db)



@app.get("/api/get_bucketLeft", response_model= float,tags=["Get"])
async def get_bucketLeft(user: schemas.Users = _fastapi.Depends(services.get_current_user),
                     db: _orm.Session = _fastapi.Depends(services.get_db),):
    return await services.get_bucketLeft(user,db)

   
   
@app.get("/api/get_volumes_per_organization", response_model= List[schemas.Volumes],tags=["Get"])
async def get_volumes_per_organization(user: schemas.Users = _fastapi.Depends(services.get_current_user),
                     db: _orm.Session = _fastapi.Depends(services.get_db),):
    return await services.get_volumes_per_organization(user,db)

   
@app.get("/api/get_volume/{volume_id}", status_code=200,tags=["Get"])
async def get_volume(
    volume_id: int,
    user: schemas.Users = _fastapi.Depends(services.get_current_user),
    db: _orm.Session = _fastapi.Depends(services.get_db),
):
    return await services.get_volume2(volume_id,user, db)   


@app.post("/api/create_requestForDeleteVolume",tags=["Post"])
async def create_requestForDeleteVolume(
    request: schemas.DeleteVolumeRequestsCreate,
    user:schemas.Users=_fastapi.Depends(services.get_current_user),
    db: _orm.Session = _fastapi.Depends(services.get_db),
    
):
    request = await services.create_requestForDeleteVolume(user,request,db)
    return {"message", "Successfully created"}



@app.get("/api/get_DeleteVolumeRequests", response_model=List[schemas.DeleteVolumeRequests],tags=["Get"])
async def get_DeleteVolumeRequests(
    user: schemas.Users = _fastapi.Depends(services.get_current_user),
    db: _orm.Session = _fastapi.Depends(services.get_db),
):
    return await services.get_DeleteVolumeRequests(architect=user, db=db)

    
@app.delete("/api/DeleteVolume_Approved/{request_id}",tags=["Delete"])
async def DeleteVolume_Approved(request_id: int,
                        architect: schemas.Users = _fastapi.Depends(services.get_current_user),
                        db: _orm.Session = _fastapi.Depends(services.get_db),
    
):
        request = await services.DeleteVolume_Approved(request_id,architect,db)
        return {"message", "Successfully deleted"}                          


@app.put("/api/DeleteVolume_Denied/{request_id}",tags=["Put"])
async def DeleteVolume_Denied(request_id: int,
                        architect: schemas.Users = _fastapi.Depends(services.get_current_user),
                        db: _orm.Session = _fastapi.Depends(services.get_db),
    
):
        request = await services.DeleteVolume_Denied(request_id,architect,db)  
        return {"message", "delete denied"}        



@app.get("/api/get_all_volumes", response_model= List[schemas.Volumes],tags=["Get"])
async def get_all_volumes(user: schemas.Users = _fastapi.Depends(services.get_current_user),
                          db: _orm.Session = _fastapi.Depends(services.get_db),):
    return await services.get_all_volumes(user,db)


@app.get("/api/recFunc/{volume_id}",tags=["Get"])
async def recFunc(volume_id:int,
                  user: schemas.Users = _fastapi.Depends(services.get_current_user),
                          db: _orm.Session = _fastapi.Depends(services.get_db),):
     data = await services.recFunc(user,volume_id,db)
     print(data)
     return data





