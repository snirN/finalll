import React, { useContext, useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from "./components/Header";
import Login from "./components/login/Login";
import { UserContext } from "./context/UserContext";
import ManagerNavbar from "./components/Navbar/ManagerNavbar";
import CreateUser from "./components/CreateUser";
import Volumes from "./components/Volumes";
import DeleteRequests from "./components/DeleteRequests";
import BucketRequests from "./components/BucketRequests";
import OrganizationsList from "./components/OrganizationsList";
import ArchitectNavbar from "./components/Navbar/ArchitectNavbar";
import UserNavbar from "./components/Navbar/UserNavbar";
import AllVolumes from "./components/AllVoumes";
import CreateBucketRequest from "./components/CreateBucketRequest";
import Users from "./components/Users";




const App = () => {
  const [token] = useContext(UserContext);
  const [role, setRole] = useState("");
  const [bucket, setBucket] = useState(0);
  const [bucketLeft, setBucketLeft] = useState(0);


  const getBucket = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/api/get_bucket", requestOptions);
      const data = await response.json();
      setBucket(data);
  };


  
  const getBucketLeft = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/api/get_bucketLeft", requestOptions);
      const data = await response.json();
      setBucketLeft(data);
  };
  
  const getRole = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/api/get_user_role", requestOptions);
      const data = await response.json();
      setRole(data);
  };



    useEffect(() => {
      if (token) {
        getRole();
        getBucket();
        getBucketLeft();
      }
    }, [token]);

  return (
    <div>
      <Router>
      <Header/>
     
     
      

      {!token ? (
            <div className="columns">
               <Login/>
            </div>
          ) : (
            
<>
            <p class ="has-text-weight-bold">  bucket left/bucket</p>
            <p class ="has-text-weight-bold">   {JSON.stringify(bucketLeft)}/{JSON.stringify(bucket)}  </p>
            <progress class="progress is-large is-link"value={bucketLeft} max={bucket} ></progress>
      
        {role === 3 && (<div>
          <UserNavbar />
          <Routes>
            <Route path="/Volumes" element={<Volumes  getBucket={getBucket} getBucketLeft={getBucketLeft}/>} />
          </Routes>
          </div>
        )}
            <div>
        {role === 2 && (<div>
          <ArchitectNavbar/>
          <Routes>
          <Route path="/Users" element={<Users />} />
          <Route path="/CreateBucketRequest" element={<CreateBucketRequest />} />
          <Route path="/DeleteRequests" element={<DeleteRequests getBucketLeft={getBucketLeft} />} />
            <Route path="/CreateUser" element={<CreateUser />} />
            <Route path="/Volumes" element={<Volumes  getBucket={getBucket} getBucketLeft={getBucketLeft}/>} />
          </Routes>
          </div>
        )}

        {role === 1 && (<div>
          <ManagerNavbar />
          <Routes>
          <Route path="/AllVolumes" element={<AllVolumes />} />
            <Route path="/BucketRequests" element={<BucketRequests/>} />
            <Route path="/OrganizationsList" element={<OrganizationsList />} />
          </Routes>
         </div>
        )}
            </div>
            </>
          )}
          
        </Router>
    </div>
  );
}


export default App;
