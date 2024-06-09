import React, { useContext, useEffect, useState } from "react";

import VolumeModel from "./VolumeModel";
import { UserContext } from "../context/UserContext";

const Volumes = ({ getBucket, getBucketLeft }) => {
  const [token] = useContext(UserContext);
  const [volumes, setVolumes] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [CreateActiveModal, setCreateActiveModal] = useState(false);
  const [IncreaseActiveModal, setIncreaseActiveModal] = useState(false);
  const [DecreaseActiveModal, setDecreaseActiveModal] = useState(false);
  const [DeleteActiveModal, setDeleteActiveModal] = useState(false);
  const [RecursiveActiveModal, setRecursiveActiveModal] = useState(false);

  const [id, setId] = useState(null);


  
  const handleIncrease = async (id) => {
    setId(id);
    setIncreaseActiveModal(true);
  };

  
  const handleDecrease = async (id) => {
    setId(id);
    setDecreaseActiveModal(true);
  };

  const handleDelete = async (id) => {
    setId(id);
    setDeleteActiveModal(true);
  };

  const handleRecursive = async (id) => {
    setId(id);
    setRecursiveActiveModal(true);
  };

  const getVolumes = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/api/get_volumes_per_organization", requestOptions);
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
    getBucket();
    getBucketLeft();
  }, []);


  
  const handleHideModal = () => {
    setCreateActiveModal(false);
    setIncreaseActiveModal(false);
    setDecreaseActiveModal(false);
    setDeleteActiveModal(false);
    setRecursiveActiveModal(false);
    getVolumes();
    setId(null);
  };

  return (
    <>
     <VolumeModel
        CreateActive={CreateActiveModal}
        IncreaseActiveModal = {IncreaseActiveModal}
        DecreaseActiveModal = {DecreaseActiveModal}
        DeleteActiveModal = {DeleteActiveModal}
        RecursiveActiveModal = {RecursiveActiveModal}
        handleHideModal={handleHideModal}
        token={token}
        id={id}
        errorMessage = {errorMessage}
        setErrorMessage={setErrorMessage}
        getBucket = {getBucket}
        getBucketLeft = {getBucketLeft}
      />
  <h1 class="title is-1 has-text-centered">Volumes </h1>    
  <button
        className="button is-fullwidth mb-5 is-primary"
        onClick={() => setCreateActiveModal(true)}
      >
        Create volume
      </button>

      {loaded && volumes ? (
        <table className="table is-fullwidth">
          <thead>
            <tr>
              <th>name</th>
              <th>size</th>
              <th>volume_real_id</th>
              <th>Actions</th>

            </tr>
          </thead>
          <tbody>
            {volumes.map((volume) => (
              <tr key={volume.volume_id}>
                <td>{volume.volume_name}</td>
                <td>{volume.size}</td>
                <td>{volume.volume_real_id}</td>
             
                <td>
                <button
                    className="button mr-2 is-info is-light"
                    onClick={() => handleIncrease(volume.volume_id)}
                  >
                    Increase
                  </button>

                  <button
                    className="button mr-2 is-info is-light"
                    onClick={() => handleDecrease(volume.volume_id)}
                  >
                    Decrese
                  </button>

                  <button
                    className="button mr-2 is-danger is-light"
                    onClick={() => handleDelete(volume.volume_id)}
                  >
                    Delete
                  </button>

                  <button
                    className="button mr-2 is-success is-light"
                    onClick={() => handleRecursive(volume.volume_id)}
                  >
                    suffix statistics
                  </button>
                  
                  
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

export default Volumes;