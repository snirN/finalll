import requests
import json
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import time
import pprint
load_dotenv()

# Authentication credentials
username = os.getenv("username1")
password = os.getenv("password")

# Base URL for the ONTAP API
base_url = os.getenv("base_url")


# Authentication
auth = (username, password)



def recFunc(volume_real_id):
    list_volumes_endpoint = f"{base_url}storage/volumes"
     # Make a GET request to list all volumes
    response = requests.get(list_volumes_endpoint, auth=auth,verify=False)

  
    # Check if the request was successful
    if response.status_code == 200:
        volumes = response.json()["records"]
        for volume in volumes:
            if volume["uuid"] == volume_real_id:
                volume_uuid = volume["uuid"]
                break
        else:
            print(f"Volume '{volume_real_id}' not found.")
            exit()

    file_counts = {
    }
    file_extention = ""
    # Construct the endpoint URL to list files and directories at the root
    root_endpoint = f"{base_url}storage/volumes/{volume_uuid}/files/"

     # Function to traverse directories and count files recursively
    def traverse_directory(endpoint, auth):
        response = requests.get(endpoint, auth=auth, verify=False)
        if response.status_code == 200:
            files = response.json()["records"]
            for file in files:
                if file["type"] == 'file':
                    file_name = file["name"]
                    file_extention = file_name.split(".")[1] #gets the extention
                    if file_counts.get(file_extention) is None:  #if extention not exist add it to dict
                        file_counts.__setitem__(file_extention,1)
                    else:
                        file_counts[file_extention] += 1
                elif file["type"] == 'directory' and file["name"]!='.' and file["name"]!='..' and file["name"]!='.snapshot':
                    dir_name = file["name"]
                    if endpoint.split("/")[-1] == "":
                        new_endpoint = f"{endpoint}{dir_name}"
                    else:
                        new_endpoint = f"{endpoint}%2F{dir_name}"
                    traverse_directory(new_endpoint, auth)  # Recursively traverse subdirectories
        else:
            print(f"Failed to retrieve files from {endpoint}. Status code: {response.status_code}")
            print("Response:", response.text)

    # Make the initial GET request to retrieve file information
    traverse_directory(root_endpoint, auth)

     # Print the final counts
    print("File counts:", file_counts)      
    return file_counts

def delete(volume_real_id):
    
    list_volumes_endpoint = f"{base_url}storage/volumes"
     # Make a GET request to list all volumes
    response = requests.get(list_volumes_endpoint, auth=auth,verify=False)

  
    # Check if the request was successful
    if response.status_code == 200:
        volumes = response.json()["records"]
        for volume in volumes:
            if volume["uuid"] == volume_real_id:
                volume_uuid = volume["uuid"]
                share_name = volume["name"]
                break
        else:
            print(f"Volume '{volume_real_id}' not found.")
            exit()

        # Define the endpoint for deleting the volume by UUID
        delete_endpoint = f"{base_url}storage/volumes/{volume_uuid}"

        # Make a DELETE request to delete the volume
        delete_response = requests.delete(delete_endpoint, auth=auth,verify=False)

        # Check if the deletion request was successful
        if delete_response.status_code == 202:
            print(f"Volume '{volume_real_id}' deleted successfully.")
        else:
            print(f"Failed to delete Volume '{volume_real_id}'. Status code: {delete_response.status_code}")
            print(delete_response.text)  # Print error message if any

    else:
        print("Failed to retrieve volume list.")      
        
    svm_endpoint = f'{base_url}/svm/svms'
    svm_name ="svm2"
    # Send the GET request to retrieve SVM information
    try:
        response = requests.get(svm_endpoint, auth=auth,verify=False)

        if response.status_code == 200:
            data = response.json()
            print("Data received from API:", data)  # Add logging to see the received data
            svm_uuid = None

            # Ensure we have 'records' key in the response
            if 'records' in data:
                # Filter the SVMs by name
                for svm in data['records']:
                    if svm['name'] == svm_name:
                        svm_uuid = svm['uuid']
                        break
                
                if svm_uuid:
                    print(f"SVM UUID for '{svm_name}': {svm_uuid}")
                else:
                    print(f"No SVM found with the name: {svm_name}")
            else:
                print("No 'records' key found in the response. Check the API response structure.")
        else:
            print(f"Failed to retrieve SVM information. Status code: {response.status_code}")
            print("Response:", response.text)  # Print response body for further investigation
    except Exception as e:
        print("An error occurred:", str(e))



    svm2 = svm_uuid
    delete_endpoint = f"{base_url}protocols/cifs/shares/{svm2}/{share_name}"

    # Make a DELETE request to delete the share
    delete_response = requests.delete(delete_endpoint, auth=auth,verify=False)

    # Check if the deletion request was successful
    if delete_response.status_code == 200:
        print(f"share '{share_name}' deleted successfully.")
    else:
        print(f"Failed to delete share '{share_name}'. Status code: {delete_response.status_code}")
        print(delete_response.text)  # Print error message if any    
      








def create(volume_name,size):   
# Authenticate and create the volume

        
    volume_data = {
        "svm.name": "svm2",
        "name": volume_name,
        "aggregates.name" :["aggr_1"],
        "size" : str(int(size))+"mb",
        "nas.path": "/" + volume_name

    }

    # Headers for authentication and content type
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post((base_url + 'storage/volumes'), headers=headers, auth= auth, data=json.dumps(volume_data),verify=False)
        if response.status_code == 202:  # HTTP status code for "Created"
                print("Volume created successfully.")
          #sleep so he post method will have enough time to update the volumes
                time.sleep(5)
                list_volumes_endpoint = f"{base_url}storage/volumes"
                # Make a GET request to list all volumes
                response = requests.get(list_volumes_endpoint, auth=auth,verify=False)
                if response.status_code == 200:
                    volumes = response.json()["records"]
                    for volume in volumes:
                        if volume["name"] == volume_name:
                            volume_uuid = volume["uuid"]
                            break
                    else:
                        print(f"Volume '{volume_name}' not found.")
                        exit() 
                                
          
            
        else:
            print("Failed to create volume. Status code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("An error occurred:", str(e))




    # JSON payload for creating a CIFS share
    cifs_share_data = {
        "svm.name": "svm2",  
        "name": volume_name,    # Name of the CIFS share
        "path": "/" + volume_name # Path in the owning SVM namespace that is shared through this share
    
    }

    # Headers for authentication and content type
    headers = {
        'Content-Type': 'application/json',
    }

    # Authenticate and create the CIFS share
    try:
        response = requests.post(base_url + 'protocols/cifs/shares', headers=headers, auth=(username, password), data=json.dumps(cifs_share_data),verify=False)
        
        # Check if the share was created successfully
        if response.status_code == 201:  # HTTP status code for "Created"
            print("CIFS share created successfully.")
            return volume_uuid
        else:
            print("Failed to create CIFS share. Status code:", response.status_code)
            print("Response:", response.text)  # Print response body for further investigation
    except Exception as e:
        print("An error occurred:", str(e))



def update(volume_id,size):

    list_volumes_endpoint = f"{base_url}storage/volumes"
     # Make a GET request to list all volumes
    response = requests.get(list_volumes_endpoint, auth=auth,verify=False)

  
    # Check if the request was successful
    if response.status_code == 200:
        volumes = response.json()["records"]
        for volume in volumes:
            if volume["uuid"] == volume_id:
                volume_uuid = volume["uuid"]
                break
        else:
            print(f"Volume '{volume_id}' not found.")
            exit()

    

    # JSON payload for updating the volume size
    update_data = {
    "size": str(int(size))+"mb"
    }

    # Headers for authentication and content type
    headers = {
    'Content-Type': 'application/json',
    }

    # Send the PUT request to update the volume size
    try:
        response = requests.patch(base_url + f'storage/volumes/{volume_uuid}', headers=headers, auth=(username, password), data=json.dumps(update_data),verify=False)

        # Check if the request was successful
        if response.status_code == 202:  # HTTP status code for "OK"
            print("Volume size updated successfully.",response.text)
        else:
            print("Failed to update volume size. Status code:", response.status_code)
            print("Response:", response.text)  # Print response body for further investigation
    except Exception as e:
        print("An error occurred:", str(e))