import React, { useContext, useState } from "react";

import { UserContext } from "../context/UserContext";
import ErrorMessage from "./messages/ErrorMessage";
import SuccsessMessage from "./messages/SuccsessMessage";


const CreateBucketRequest = () => {
  const [size, setSize] = useState("");
  const [details, setDetails] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const[succsessMessage,setSuccsessMessage] = useState("");
  const [token] = useContext(UserContext);

  const submitRequest = async () => {
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
         details: details,
         size: size }),
    };

    const response = await fetch("/api/create_request_For_Increase_Bucket", requestOptions);
  

    if (!response.ok) {
      setErrorMessage("failed to make request");
      setSuccsessMessage("");
    } 
    else{
        setErrorMessage("");
        setSuccsessMessage("request added.");
        cleanFormData();
    }

 
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (size > 5 && size<300) {
      submitRequest();
    } else {
      setErrorMessage("Ensure that the size greater than 5 and less than 300");
      setSuccsessMessage("");
    }
  };


  
  const cleanFormData = () => {
    setDetails("");
    setSize("");

  };

  return (
    <div className="column">
      <form className="box" onSubmit={handleSubmit}>
        <h1 className="title has-text-centered"> Create Bucket Request</h1>
        <div className="field">
          <label className="label">Size</label>
          <div className="control">
            <input
              type="number"
              placeholder="Enter size"
              value={size}
              onChange={(e) => setSize(e.target.value)}
              className="input"
              required
              min={5}
              max={300}

            />
          </div>
        </div>
        <div className="field">
          <label className="label">Details</label>
          <div className="control">
            <input
              type="text"
              placeholder="Enter Details"
              value={details}
              onChange={(e) => setDetails(e.target.value)}
              className="input"
              maxLength={20}
            />
          </div>
        </div>
        <ErrorMessage message={errorMessage} />
        <SuccsessMessage message={succsessMessage}/>
        <br />
        <button className="button is-primary" type="submit">
          Create Request
        </button>
      </form>
    </div>
  );
};

export default CreateBucketRequest;