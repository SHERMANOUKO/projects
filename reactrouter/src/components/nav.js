import React from 'react';
import '../App.css';
import {Link} from 'react-router-dom';

function Nav() {
    const navStyle = {
        color: 'white'
    }

    return (
        <nav>
            <ul className="navLinks">
                <Link to="/about" style={navStyle}>
                    <li>About</li>
                </Link>
                <Link to="/shop" style={navStyle}>
                    <li>Shop</li>  
                </Link>
            </ul> 
        </nav>
    );
}

export default Nav;
