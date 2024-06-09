import React, { useContext, useEffect, useState } from "react";
import moment from "moment";

import ErrorMessage from "./messages/ErrorMessage";
import { UserContext } from "../context/UserContext";
import SuccsessMessage from "./messages/SuccsessMessage";

const BucketRequests = () => {
  const [token] = useContext(UserContext);
  const [BucketRequests, setBucketRequests] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [succsessMessage, setSuccsessMessage] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [id, setId] = useState(null);



  const getBucketRequests = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/api/bucketRequests", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the requests");
      setSuccsessMessage("");
    } else {
      const data = await response.json();
      setBucketRequests(data);
      setLoaded(true);
    }
  };


  useEffect(() => {
    getBucketRequests();
  },[id]);
  
  const handleApproved = async (request_id) => {
    const requestOptions = {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
     

    };
    const response = await fetch(`/api/update_Bucket_Approved/${request_id}`, requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong when try to approve");
      setSuccsessMessage("");
    } else {
      setErrorMessage("");
      setSuccsessMessage("approved");
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
    const response = await fetch(`/api/update_Bucket_Denied/${request_id}`, requestOptions);
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
    <h1 class="title is-1 has-text-centered">Bucket increase requests </h1>

    <ErrorMessage message={errorMessage} />
    <SuccsessMessage message={succsessMessage} />
         {loaded && BucketRequests ? (
           <table className="table is-fullwidth">
             <thead>
               <tr>
                 <th>request_date</th>
                 <th>architect_id</th>
                 <th>size</th>
                 <th>details</th>
                 <th>status_id</th>
                 <th>actions</th>
   
               </tr>
             </thead>
             <tbody>
               {BucketRequests.map((BucketRequest) => (
                   <tr key={BucketRequest.request_id}>
                   <td>{moment(BucketRequest.request_date).format("MMM Do YY")}</td>
                   <td>{BucketRequest.architect_id}</td>
                   <td>{BucketRequest.size}</td>
                   <td>{BucketRequest.details}</td>
                   <td>{BucketRequest.status_id}</td>
                
                   <td>
                   {BucketRequest.status_id !== 3 && BucketRequest.status_id !== 2 && ( // Render buttons only if status_id is not 3/2
                   <>
                   <button
                       className="button mr-2 is-info is-light"
                       onClick={() =>  {setId(BucketRequest.request_id);handleApproved(BucketRequest.request_id)}}
                     >
                       Accept
                     </button>
                     <button
                       className="button mr-2 is-danger is-light"
                       onClick={() =>  {setId(BucketRequest.request_id);handleDenied(BucketRequest.request_id)}}
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
  export default BucketRequests;