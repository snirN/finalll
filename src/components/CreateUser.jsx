import React, { useContext, useState } from "react";

import { UserContext } from "../context/UserContext";
import ErrorMessage from "./messages/ErrorMessage";
import SuccsessMessage from "./messages/SuccsessMessage";


const CreateUser = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmationPassword, setConfirmationPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const[succsessMessage,setSuccsessMessage] = useState("");
  const [token] = useContext(UserContext);

  const submitRegistration = async () => {
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
         email: email,
         hash_password: password }),
    };

    const response = await fetch("/api/users", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      setErrorMessage(data.detail);
      setSuccsessMessage("");

    } 
    else{
        setErrorMessage("");
        setSuccsessMessage("user added.");
        cleanFormData();
    }

 
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === confirmationPassword && password.length > 7) {
      submitRegistration();
    } else {
      setErrorMessage("Ensure that the passwords match and greater than 8 characters");
      setSuccsessMessage("");

      
    }
  };

  
  const cleanFormData = () => {
    setEmail("");
    setPassword("")
    setConfirmationPassword("");

  };

  return (
    <div className="column">
      <form className="box" onSubmit={handleSubmit}>
        <h1 className="title has-text-centered"> Create User</h1>
        <div className="field">
          <label className="label">Email Address</label>
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
          <label className="label">Password</label>
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
          <label className="label">Confirm Password</label>
          <div className="control">
            <input
              type="password"
              placeholder="Enter password"
              value={confirmationPassword}
              onChange={(e) => setConfirmationPassword(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <ErrorMessage message={errorMessage} />
        <SuccsessMessage message={succsessMessage}/>
        <br />
        <button className="button is-primary" type="submit">
          Create User
        </button>
      </form>
    </div>
  );
};

export default CreateUser;