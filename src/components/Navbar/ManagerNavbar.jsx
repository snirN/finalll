import { useNavigate } from "react-router-dom";


const ManagerNavbar  = () => {
    const navigate = useNavigate();

    const handleNavigate = (path) => {
        navigate(path);
    };
    return (  <nav  className="navbar is-info" role="navigation" aria-label="main navigation">
        <div id="navbarBasicExample" className="navbar-menu">
                <div className="navbar-start">
                <a className="navbar-item" onClick={() => handleNavigate('/AllVolumes')}>
                    All Volumes
                    </a>
                    <a className="navbar-item" onClick={() => handleNavigate('/BucketRequests')}>
                    Bucket Requests
                    </a>
                    <a className="navbar-item" onClick={() => handleNavigate('/OrganizationsList')}>
                    Organizations List
                    </a>
                </div>
            </div>

    </nav>

     );
}
 
export default ManagerNavbar;