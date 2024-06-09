import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";

const Header = () => {
  const [token, setToken] = useContext(UserContext);
  const navigate = useNavigate();



  const handleLogout = () => {
    setToken(null);
    navigate("");


  };

  return (

    <div className="has-text-centered m-6">
      <h1 className="title is-1 has-text-centered">WOS-APP</h1>
      <h2 className="title is-2 has-text-centered">World Of Storage</h2>
      {token && (
        <button className="button" onClick={handleLogout}>
          Logout
        </button>
      )}
    </div>
  );
};

export default Header;