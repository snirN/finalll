import React, { useContext, useEffect, useState } from "react";
import moment from "moment";

import ErrorMessage from "./messages/ErrorMessage";
import { UserContext } from "../context/UserContext";
import SuccsessMessage from "./messages/SuccsessMessage";

const DeleteRequests = ({getBucketLeft}) => {
  const [token] = useContext(UserContext);
  const [DeleteRequests, setDeleteRequests] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [succsessMessage, setSuccsessMessage] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [id, setId] = useState(null);



  const getDeleteRequests = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/api/get_DeleteVolumeRequests", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the requests");
      setSuccsessMessage("");
    } else {
      const data = await response.json();
      setDeleteRequests(data);
      setLoaded(true);
    }
  };

  useEffect(() => {
    getDeleteRequests();
  },[id]);


 
  const handleApproved = async (request_id) => {
    const requestOptions = {
      method: "delete",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
     

    };
    const response = await fetch(`/api/DeleteVolume_Approved/${request_id}`, requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong when try to approve");
      setSuccsessMessage("");
    } else {
      setErrorMessage("");
      setSuccsessMessage("approved");
      getBucketLeft();
    }
  };
  

  const handleDenied = async (request_id) => {
    const requestOptions = {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
     

    };
    const response = await fetch(`/api/DeleteVolume_Denied/${request_id}`, requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong when try to deny");
      setSuccsessMessage("");
    } else {
      setErrorMessage("");
      setSuccsessMessage("denied");
    }
  };
  

  return (
    <>
    <h1 class="title is-1 has-text-centered">delete volume requests </h1>

    <ErrorMessage message={errorMessage} />
    <SuccsessMessage message={succsessMessage} />
         {loaded && DeleteRequests ? (
           <table className="table is-fullwidth">
             <thead>
               <tr>
                 <th>request_date</th>
                 <th>user_id</th>
                 <th>volume_id</th>
                 <th>details</th>
                 <th>status_id</th>
   
               </tr>
             </thead>
             <tbody>
               {DeleteRequests.map((DeleteRequest) => (
                 <tr key={DeleteRequest.request_id}>
                   <td>{moment(DeleteRequest.request_date).format("MMM Do YY")}</td>
                   <td>{DeleteRequest.user_id}</td>
                   <td>{DeleteRequest.volume_id}</td>
                   <td>{DeleteRequest.details}</td>
                   <td>{DeleteRequest.status_id}</td>
                
                   <td>
                   {DeleteRequest.status_id !== 3 && DeleteRequest.status_id !== 2 && ( // Render buttons only if status_id is not 3/2
                   <>
                   <button
                       className="button mr-2 is-info is-light"
                       onClick={() =>  {setId(DeleteRequest.request_id);handleApproved(DeleteRequest.request_id)}}
                     >
                       Accept
                     </button>
                     <button
                       className="button mr-2 is-danger is-light"
                       onClick={() =>  {setId(DeleteRequest.request_id);handleDenied(DeleteRequest.request_id)}}
                     >
                       Deny
                     </button>
                     </>
                     )}
                   </td>
                 </tr>
               ))}
             </tbody>
           </table>
         ) : (
           <p>Loading</p>
         )}
       </>
     );
    


};
  export default DeleteRequests;