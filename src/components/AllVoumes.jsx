import React, { useContext, useEffect, useState } from "react";

import ErrorMessage from "./messages/ErrorMessage";
import { UserContext } from "../context/UserContext";


const AllVolumes = () => {
    const [token] = useContext(UserContext);
    const [volumes, setVolumes] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);
  





const getVolumes = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/api/get_all_volumes", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the volumes");
    } else {
      const data = await response.json();
      setVolumes(data);
      setLoaded(true);

    }
  };

  useEffect(() => {
    getVolumes();
  }, []);

  
  return (
    <>
  
  <h1 class="title is-1 has-text-centered">All Volumes </h1>    

 <ErrorMessage message={errorMessage} />
      {loaded && volumes ? (
        <table className="table is-fullwidth">
          <thead>
            <tr>
              <th>name</th>
              <th>size</th>
              <th>volume_real_id</th>
              <th>organization_id</th>


            </tr>
          </thead>
          <tbody>
            {volumes.map((volume) => (
              <tr key={volume.id}>
                <td>{volume.volume_name}</td>
                <td>{volume.size}</td>
                <td>{volume.volume_real_id}</td>
                <td>{volume.organization_id}</td>
             
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

export default AllVolumes;