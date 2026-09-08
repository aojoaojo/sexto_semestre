import { Link, Outlet } from 'react-router'
import logo from '../assets/logo.png'
import '../global.css'

export function Layout() {
    return (
        <div>
            <nav className="navbar navbar-expand-lg bg-verde-4 p-0 m-0">
                <div className="container-fluid d-flex align-items-center p-3">
                    <Link className='navbar-brand d-flex justify-content-center align-items-center' to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                        <a className="navbar-brand" href="#">
                            <div className='d-flex flex-column justify-content-center'>
                                <img src={logo} alt="logo" height={80} />
                                <p className='m-0'>Farmework</p>
                            </div>
                        </a>
                    </Link>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            <li className="nav-item">
                                <Link to="/sobre" style={{ textDecoration: 'none', color: 'inherit' }}>
                                    <a className="nav-link active" aria-current="page" href="#">Sobre Nós</a>
                                </Link>
                            </li>
                            <li className="nav-item">
                                <Link to="/servicos" style={{ textDecoration: 'none', color: 'inherit' }}>
                                    <a className="nav-link" href="#">Nossos Serviços</a>
                                </Link>
                            </li>
                            {/* <li className="nav-item dropdown">
                                <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    Dropdown
                                </a>
                                <ul className="dropdown-menu">
                                    <li>
                                        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                                            <a className="dropdown-item" href="#">Action</a>
                                        </Link>
                                    </li>
                                    <li>
                                        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                                            <a className="dropdown-item" href="#">Action</a>
                                        </Link>
                                    </li>
                                    <li>
                                        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                                            <a className="dropdown-item" href="#">Action</a>
                                        </Link>
                                    </li>
                                    <li>
                                        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                                            <a className="dropdown-item" href="#">Action</a>
                                        </Link>
                                    </li>
                                </ul>
                            </li>
                            <li className="nav-item">
                                <Link to="/contato" style={{ textDecoration: 'none', color: 'inherit' }}>
                                    <a className="nav-link" href="#">Contato</a>
                                </Link>
                            </li> */}
                        </ul>
                        <form className="d-flex" role="search">
                            <input className="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
                            <button className="btn btn-outline-success" type="submit">Search</button>
                        </form>
                    </div>
                </div>
            </nav>
            <Outlet />
        </div>
    )
}