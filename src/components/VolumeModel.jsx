import React, { useEffect, useState } from "react";
import ErrorMessage from "./messages/ErrorMessage";

const VolumeModel = ({ CreateActive,IncreaseActiveModal,DecreaseActiveModal,DeleteActiveModal,RecursiveActiveModal,
   handleHideModal, token, id,errorMessage, setErrorMessage, getBucket, getBucketLeft }) => {
  const [volume_name, setVolume_name] = useState("");
  const [size, setSize] = useState("");
  const [volume_id, setVolume_id] = useState("");
  const [details, setDetails] = useState("");
  const [RecursiveDetails, setRecursiveDetails] = useState({});



  useEffect(() => {
    const getVolume = async () => {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`/api/get_volume/${id}`, requestOptions);

      if (!response.ok) {
        setErrorMessage("Could not get the volume");
      } else {
        const data = await response.json();
        setErrorMessage("");
        setVolume_id(data.volume_id);
        setVolume_name(data.volume_name);
        setSize(data.size);
      }
      if(RecursiveActiveModal)
        {
          handleRecursiveFunction(id);
        }
    };

    if (id) {
      getVolume();
    }
   
  }, [id, token,RecursiveActiveModal]);





  const cleanFormData = () => {
    setVolume_name("");
    setSize("");
    setDetails("");
    setErrorMessage("");



  };

  const handleCreateVolume= async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        volume_name: volume_name,
        size: size,
      }),
    };
    const response = await fetch("/api/create_volume", requestOptions);
    const data = await response.json();
    if (!response.ok) {
      setErrorMessage(data.detail);
    } else {
      setErrorMessage("");
      cleanFormData();
      handleHideModal();
      getBucket();
      getBucketLeft();
      
    }
  };

  const handleIncreaseSize = async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },

    };
    const response = await fetch(`/api/volumeSizeIncrease/${volume_id}/${size}`, requestOptions);
    const data = await response.json();
    if (!response.ok) {
      setErrorMessage(data.detail);

    } else {
      setErrorMessage("");
      cleanFormData();
      handleHideModal();
      getBucket();
      getBucketLeft();
    }
  };



  const handleDecreaseSize = async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch(`/api/volumeSizeDecrease/${volume_id}/${size}`, requestOptions);
    const data = await response.json();

    if (!response.ok) {
      setErrorMessage(data.detail);

    } else {
      setErrorMessage("");
      cleanFormData();
      handleHideModal();
      getBucket();
      getBucketLeft();
    }
  };


  const handleDeleteRequest= async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        volume_id: volume_id,
        details: details,
      }),
    };
    const response = await fetch("/api/create_requestForDeleteVolume", requestOptions);
    const data = await response.json();
    if (!response.ok) {
      setErrorMessage(data.detail);
    } else {
      setErrorMessage("");
      cleanFormData();
      handleHideModal(); 
           
    }
  };



  const handleRecursiveFunction = async (id) => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch(`/api/recFunc/${id}`, requestOptions);

    if (!response.ok) {
      setErrorMessage("Could not get the data");
    } else {
      const data = await response.json();
      setErrorMessage("");
      setRecursiveDetails((data));
    }
  };


  
 

  return (

<div>
    <div className={`modal ${CreateActive && "is-active"}`}>
      <div className="modal-background" onClick={handleHideModal}></div>
      <div className="modal-card">
        <header className="modal-card-head has-background-primary-light">
          <h1 className="modal-card-title">
             Create volume
          </h1>
        </header>
        <section className="modal-card-body">
        <ErrorMessage message={errorMessage} />
          <form>
            <div className="field">
              <label className="label"> Name</label>
              <div className="control">
                <input
                  type="text"
                  placeholder="Enter first name"
                  value={volume_name}
                  onChange={(e) => setVolume_name(e.target.value)}
                  className="input"
                  required
                  maxLength={20} 
                />
              </div>
            </div>
            <div className="field">
              <label className="label">size</label>
              <div className="control">
                <input
                  type="number"
                  placeholder="Enter size"
                  value={size}
                  onChange={(e) => setSize(e.target.value)}
                  className="input"
                  required
                  min={20}
                  max={100}
                />
              </div>
            </div>
          </form>
        </section>
        <footer className="modal-card-foot has-background-primary-light">
            <button className="button is-primary" onClick={handleCreateVolume}>
              Create
            </button>
          <button className="button" onClick={() => { cleanFormData();handleHideModal();}}>
            Cancel
          </button>
        </footer>
      </div>
    </div>



    <div className={`modal ${IncreaseActiveModal && "is-active"}`}>
      <div className="modal-background" onClick={handleHideModal}></div>
      <div className="modal-card">
        <header className="modal-card-head has-background-info-light">
          <h1 className="modal-card-title">
             Increase size
          </h1>
        </header>
        <section className="modal-card-body">
        <ErrorMessage message={errorMessage} />
          <form>
            <div className="field">
              <label className="label">size</label>
              <div className="control">
                <input
                  type="number"
                  placeholder="Enter size"
                  value={size}
                  onChange={(e) => setSize(e.target.value)}
                  className="input"
                  required
                  min={20}
                  max={100}
                />
              </div>
            </div>
          </form>
        </section>
        <footer className="modal-card-foot has-background-info-light">
            <button className="button is-info" onClick={handleIncreaseSize}>
              Increase
            </button>
          <button className="button" onClick={() => { cleanFormData();handleHideModal();}}>
            Cancel
          </button>
        </footer>
      </div>
    </div>






    

    <div className={`modal ${DecreaseActiveModal && "is-active"}`}>
      <div className="modal-background" onClick={handleHideModal}></div>
      <div className="modal-card">
        <header className="modal-card-head has-background-info-light">
          <h1 className="modal-card-title">
             Decrease size
          </h1>
        </header>
        <section className="modal-card-body">
        <ErrorMessage message={errorMessage} />
          <form>
            <div className="field">
              <label className="label">size</label>
              <div className="control">
                <input
                  type="number"
                  placeholder="Enter size"
                  value={size}
                  onChange={(e) => setSize(e.target.value)}
                  className="input"
                  required
                  min={20}
                  max={100}
                />
              </div>
            </div>
          </form>
        </section>
        <footer className="modal-card-foot has-background-info-light">
            <button className="button is-info" onClick={handleDecreaseSize}>
              Decrease
            </button>
          <button className="button" onClick={() => { cleanFormData();handleHideModal();}}>
            Cancel
          </button>
        </footer>
      </div>
    </div>


    
    <div className={`modal ${DeleteActiveModal && "is-active"}`}>
      <div className="modal-background" onClick={handleHideModal}></div>
      <div className="modal-card">
        <header className="modal-card-head has-background-danger-light">
          <h1 className="modal-card-title">
             Delete request
          </h1>
        </header>
        <section className="modal-card-body">
        <ErrorMessage message={errorMessage} />
          <form>
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
          </form>
        </section>
        <footer className="modal-card-foot has-background-danger-light">
            <button className="button is-danger" onClick={handleDeleteRequest}>
              Submit
            </button>
          <button className="button" onClick={() => { cleanFormData();handleHideModal();}}>
            Cancel
          </button>
        </footer>
      </div>
    </div>



    <div className={`modal ${RecursiveActiveModal && "is-active"}`}>
      <div className="modal-background" onClick={handleHideModal}></div>
      <div className="modal-card">
        <header className="modal-card-head has-background-success-light">
          <h1 className="modal-card-title">
             suffix statistics
          </h1>
        </header>
        <section className="modal-card-body">
        <ErrorMessage message={errorMessage} />
          <form>
            <div className="field">
            <label className="label">Details</label>
            <div>
              <p>{Object.entries(RecursiveDetails).map(([ext,count])=>(
                <li key={ext}>{ext}: {count}</li>
              ))}</p>

            </div>
            </div>
          </form>
        </section>
        <footer className="modal-card-foot has-background-success-light">
          <button className="button" onClick={() => { cleanFormData();handleHideModal();}}>
            Cancel
          </button>
        </footer>
      </div>
    </div>
</div>
  );
};

export default VolumeModel;