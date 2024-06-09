import { useNavigate } from "react-router-dom";


const ArchitectNavbar  = () => {
    const navigate = useNavigate();

    const handleNavigate = (path) => {
        navigate(path);
    };
    return (  <nav  className="navbar is-info" role="navigation" aria-label="main navigation">
        <div id="navbarBasicExample" className="navbar-menu">
                <div className="navbar-start">
                    <a className="navbar-item" onClick={() => handleNavigate('/Users')}>
                    Users
                    </a>
                    <a className="navbar-item" onClick={() => handleNavigate('/CreateBucketRequest')}>
                    Create Bucket Request
                    </a>
                    <a className="navbar-item" onClick={() => handleNavigate('/DeleteRequests')}>
                    Delete Requests
                    </a>
                    <a className="navbar-item" onClick={() => handleNavigate('/CreateUser')}>
                    Create User
                    </a>
                    <a className="navbar-item" onClick={() => handleNavigate('/Volumes')}>
                    Volumes
                    </a>
                </div>
            </div>

    </nav>

     );
}
 
export default ArchitectNavbar;