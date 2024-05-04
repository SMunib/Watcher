import React, { useState,useRef } from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import { Link, useNavigate } from 'react-router-dom';
import { AiOutlineHome, AiOutlineUser } from 'react-icons/ai';
import logo from '../assets/netflix1.png';
import videoSource from '../assets/trailer/Endgame.mp4';


export default function Home() {
  const navigate = useNavigate();
  const [expand, updateExpanded] = useState(false);
  const [navColour, updateNavbar] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  function scrollHandler() {
    if (window.scrollY >= 20) {
      updateNavbar(true);
    } else {
      updateNavbar(false);
    }
  }

  window.addEventListener('scroll', scrollHandler);

  const handleSearchInputChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSearch = () => {
    // Perform search logic here
    console.log('Searching for:', searchQuery);
  };
  
  const movies = [
    {
      name: "The Shawshank Redemption",
      picturePath: "../assets/Endgame.jpg"
    },
    {
      name: "The Godfather",
      picturePath: "../assets/Endgame.jpg"
    },
    {
      name: "The Dark Knight",
      picturePath: "../assets/Endgame.jpg"
    },
    {
      name: "Schindler's List",
      picturePath: "../assets/Endgame.jpg"
    },
    {
      name: "Pulp Fiction",
      picturePath: "../assets/Endgame.jpg"
    },
    {
      name: "Forrest Gump",
      picturePath: "../assets/Endgame.jpg"
    },
    {
      name: "Inception",
      picturePath: "../assets/mov.jpg"
    },
    {
      name: "The Matrix",
      picturePath: "../assets/Endgame.jpg"
    },
    {
      name: "Interstellar",
      picturePath: "../assets/Endgame.jpg"
    },
    {
      name: "Fight Club",
      picturePath: "../assets/Endgame.jpg"
    }
  ];
  

  return (
    <div className="mainn">
      <Navbar
        expanded={expand}
        fixed="top"
        expand="md"
        className={navColour ? 'sticky' : 'navbar'}
      >
        <Container>
          <Navbar.Brand as={Link} to="/" className="d-flex">
            <img src={logo} className="img-fluid logo" alt="brand" />
          </Navbar.Brand>

          <Navbar.Toggle
            aria-controls="responsive-navbar-nav"
            onClick={() => {
              updateExpanded(expand ? false : 'expanded');
            }}
          >
            <span></span>
            <span></span>
            <span></span>
          </Navbar.Toggle>
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="ms-auto" defaultActiveKey="#home">
              <Nav.Item className="search-bar">
                <input
                  type="text"
                  placeholder="Search..."
                  value={searchQuery}
                  onChange={handleSearchInputChange}
                />
                <button className="search-button" onClick={handleSearch}>
                  Search
                </button>
              </Nav.Item>
              
              <Nav.Item>
                <Nav.Link
                  as={Link}
                  to="/about"
                  onClick={() => updateExpanded(false)}
                >
                  <AiOutlineUser style={{ marginBottom: '2px' }} /> About
                </Nav.Link>
              </Nav.Item>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar> 
      <div className="movie">
        <video controls autoPlay loop>
          <source src={videoSource} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
      <div className="movie-container">
        <div className="movie-list">
          {movies.map((movie, index) => (
            <div key={index} className="movie-item">
              <img src={movie.picturePath} alt={movie.name} />
            </div>
          ))}
        </div>
      </div>

      
 

    </div>
  );
}
