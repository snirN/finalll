import pydantic
from typing import Optional
import datetime as _dt





class _OrganizationsBase(pydantic.BaseModel):
    
    organization_name: str
    bucket : float
    


class OrganizationsCreate(_OrganizationsBase):
    pass


class Organizations(_OrganizationsBase):
    organization_id: int
    bucketLeft : float

    class Config:
       from_attributes=True



class _UsersBase(pydantic.BaseModel):
    email: str


class UsersCreate(_UsersBase):
    hash_password: str
    

    class Config:
        from_attributes=True


class Users(_UsersBase):
    user_id: int
    organization_id:int
    role:int
    

    class Config:
       from_attributes=True




class _VolumesBase(pydantic.BaseModel):
    volume_name: str
    size:float


class VolumesCreate(_VolumesBase):
    pass

class Volumes(_VolumesBase):
    volume_id: int
    volume_real_id: str
    organization_id:int
    

    class Config:
       from_attributes=True





class _BucketRequestsBase(pydantic.BaseModel):
        details: Optional[str] = " "
        size:float


class BucketRequestsCreate(_BucketRequestsBase):
    pass

class BucketRequests(_BucketRequestsBase):
    architect_id: int
    request_id: int
    request_date: _dt.datetime
    status_id:int


    class Config:
       from_attributes=True






class _DeleteVolumeRequestsBase(pydantic.BaseModel):
        details: Optional[str] = " "
        volume_id:int


class DeleteVolumeRequestsCreate(_DeleteVolumeRequestsBase):
    pass

class DeleteVolumeRequests(_DeleteVolumeRequestsBase):
    user_id: int
    organization_id: int
    request_id: int
    request_date: _dt.datetime
    status_id:int


    class Config:
       from_attributes=True
