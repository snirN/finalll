import React, { useContext, useEffect, useState } from "react";

import ErrorMessage from "./messages/ErrorMessage";
import { UserContext } from "../context/UserContext";
import SuccsessMessage from "./messages/SuccsessMessage";

const OrganizationsList = () => {
  const [token] = useContext(UserContext);
  const [OrganizationsList, setOrganizationsList] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [succsessMessage, setSuccsessMessage] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [activeModal, setActiveModal] = useState(false);
  const [id, setId] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [organization_name, setOrganization_name] = useState("");
  const [bucket, setBucket] = useState("");



  const getOrganizationsList = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/api/get_organizations", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the requests");
    } else {
      const data = await response.json();
      setOrganizationsList(data);
      setLoaded(true);
    }
  };



  const CreateOrganization = async (e) => {
    e.preventDefault();
    if (password.length < 8) {
      setErrorMessage("Password must be at least 8 characters long");
    } else {
      setErrorMessage("");
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        
          architect: {
            email: email,
            hash_password: password
          },
          organization: {
            organization_name: organization_name,
            bucket: bucket
          }
        
    }),
  
    };
    const response = await fetch("/api/create_organization", requestOptions);
    const data = await response.json();
    if (!response.ok) {
      setErrorMessage(data.detail);
    } else {
      cleanFormData();
      handleModal();
      
    }
  }
  };


  
  const deleteOrganization = async (organization_id ) => {
    const requestOptions = {
      method: "delete",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
     

    };
    const response = await fetch(`/api/organizations/${organization_id}`, requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong when try to delete");
      setSuccsessMessage("");
    } else {
      setErrorMessage("");
      setSuccsessMessage("deleted.");
    }
  };
  

  useEffect(() => {
    getOrganizationsList();
  }, [id]);

  
  const cleanFormData = () => {
    setEmail("");
    setPassword("");
    setOrganization_name("");
    setBucket("");

  };

  const handleModal = () => {
    setActiveModal(!activeModal);
    getOrganizationsList();
    setId(null);
  };

  return (
    <>
    <h1 class="title is-1 has-text-centered"> Organizations </h1>
    <button
        className="button is-fullwidth mb-5 is-primary"
        onClick={() => setActiveModal(true)}
      >
        Create organizaion
      </button>
      <div className={`modal ${activeModal && "is-active"}`}>
        <div className="modal-background" onClick={handleModal}></div>
        <div className="modal-card">
          <header className="modal-card-head has-background-primary-light">
            <h1 className="modal-card-title">
              Create volume
          </h1>
        </header>
        <section className="modal-card-body">
        <ErrorMessage message={errorMessage} />
          <form >
            <div className="field">
              <label className="label"> email</label>
              <div className="control">
                <input
                  type="email"
                  placeholder="Enter email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input"
                  required
                />
              </div>
            </div>
            <div className="field">
              <label className="label"> password </label>
              <div className="control">
                <input
                  type="password"
                  placeholder="Enter password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input"
                  required
                />
              </div>
            </div>
            <div className="field">
              <label className="label"> organization_name </label>
              <div className="control">
                <input
                  type="text"
                  placeholder="Enter organization name"
                  value={organization_name}
                  onChange={(e) => setOrganization_name(e.target.value)}
                  className="input"
                  required
                  maxLength={20} 
                />
              </div>
            </div>
            <div className="field">
              <label className="label"> bucket</label>
              <div className="control">
                <input
                  type="number"
                  placeholder="Enter bucket"
                  value={bucket}
                  onChange={(e) => setBucket(e.target.value)}
                  className="input"
                  required
                  max={10000}
                  min={100}
                />
              </div>
            </div>
          </form>
        </section>
        <footer className="modal-card-foot has-background-primary-light">
            <button className="button is-primary" onClick={CreateOrganization}>
              Create
            </button>
          <button className="button" onClick={() => { cleanFormData();handleModal();}}>
            Cancel
          </button>
        </footer>
      </div>
    </div>
    <ErrorMessage message={errorMessage} />
    <SuccsessMessage message={succsessMessage} />
         {loaded && OrganizationsList ? (
           <table className="table is-fullwidth">
             <thead>
               <tr>
                 <th>organizaion_name</th>
                 <th>bucket</th>
                 <th>bucketLeft</th>
                 <th>actions</th>

   
               </tr>
             </thead>
             <tbody>
               {OrganizationsList.map((Organization) => (
                 <tr key={Organization.organization_id}>
                   <td>{Organization.organization_name}</td>
                   <td>{Organization.bucket}</td>
                   <td>{Organization.bucketLeft}</td>
                
                   <td>
                   {Organization.organization_name !== "manager" && ( 
                   <>
                     <button
                       className="button mr-2 is-danger is-light"
                       onClick={() => {setId(Organization.organization_id);deleteOrganization(Organization.organization_id)}}
                     >
                       Delete
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
  export default OrganizationsList;