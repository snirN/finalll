import React, { useContext, useEffect, useState } from "react";
import moment from "moment";

import ErrorMessage from "./messages/ErrorMessage";
import { UserContext } from "../context/UserContext";

const Users = () => {
  const [token] = useContext(UserContext);
  const [users, setUsers] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [activeModal, setActiveModal] = useState(false);
  const [id, setId] = useState(null);



  const getUsers = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/api/get_users_per_organization", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the Users");
    } else {
      const data = await response.json();
      setUsers(data);
      setLoaded(true);
    }
  };

  useEffect(() => {
    getUsers();
  }, []);




  
  const handleDelete = async (id) => {
    const requestOptions = {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch(`/api/users/${id}`, requestOptions);
    if (!response.ok) {
      setErrorMessage("Failed to delete users");
    }
    else
    setErrorMessage("");

    getUsers();
  };


  

  return (
    <>
    <h1 class="title is-1 has-text-centered">Users </h1>

    <ErrorMessage message={errorMessage} />
         {loaded && users ? (
           <table className="table is-fullwidth">
             <thead>
               <tr>
                 <th>email</th>
                 <th>actions</th>
   
               </tr>
             </thead>
             <tbody>
               {users.map((users) => (
                 <tr key={users.user_id}>
                   <td>{users.email}</td>
                
                   <td>
                   {users.role !== 2 && ( 
                   <>
                     <button
                       className="button mr-2 is-danger"
                       onClick={() => handleDelete(users.user_id)}

                     >
                       delete
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
  export default Users;