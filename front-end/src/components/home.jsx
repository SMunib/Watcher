import React, { useState, useEffect, useRef } from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import { Link ,useNavigate, useLocation } from 'react-router-dom';
import { AiOutlineUser } from 'react-icons/ai';
import logo from '../assets/netflix1.png';
import videoSource from '../assets/trailer/Endgame.mp4';
import Swiper from 'swiper';
import 'swiper/swiper-bundle.css';
import MiniPage from './minipage';
import SearchPage from './Search';
import axios from 'axios';
import { userid } from './Global';

export default function Home() {
  const [navColour, updateNavbar] = useState(false);
  const [expand, updateExpanded] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const videoRef = useRef(null);
  const [selectedImage, setSelectedImage] = useState(null);
   const navigate = useNavigate();
   const location = useLocation();
   const [selectedImage1, setSelectedImage1] = useState(null);
  //  const [videoSource, setVideoSource] = useState('');
   
  //  useEffect(() => {
  //   const fetchVideoList = async () => {
  //     try {
  //       const response = await axios.get('assets/trailer');
  //       const files = response.data;
  //       const randomVideo = files[Math.floor(Math.random() * files.length)];
  //       setVideoSource(randomVideo);
  //     } catch (error) {
  //       console.error('Axios Error:', error);
  //       console.error('Request Config:', error.config);
  //       console.error('Error Response:', error.response);
  //     }
  //   };
  
  //   fetchVideoList();
  // }, []);


   //------variables for genres-----
   const [Genre1,setGenre1]=useState([]);
   const [Genre2,setGenre2]=useState([]);
   const [Genre3,setGenre3]=useState([]);
   const [Genre4,setGenre4]=useState([]);
   const [Genre5,setGenre5]=useState([]);
   const [Genre6,setGenre6]=useState([]);
   const [Genre7,setGenre7]=useState([]);
   const [Genre8,setGenre8]=useState([]);
   const [Genre9,setGenre9]=useState([]);
   const [Genre10,setGenre10]=useState([]);

   //------get requests for sliders-------
   useEffect(() => {
    console.log(userid)
    axios.post('http://localhost:5000/movie/recommend', userid)
        .then(result => {
          console.log(result);
          setGenre1(result.data)
            // console.log(result.data.message);
        })
        .catch(err => console.log(err));

      axios.post('http://localhost:5000/movie/LastWatched',userid)
      .then(response => {
        setGenre2(response.data);
      })
      .catch(error => {
        console.error('Error fetching genres:', error);
      });
    
      axios.get('http://localhost:5000/movie/display')
      .then(response => {
        setGenre3(response.data);
      })
      .catch(error => {
        console.error('Error fetching genres:', error);
      });

      axios.post('http://localhost:5000/movie/moviesbycategory', {genre:"Crime"})
        .then(result => {
          console.log(result);
          // if (result.data.status === 200) {
            setGenre4(result.data)
            // console.log(result.data.message);
            
          // } else {
          //   alert(result.data.message);
          // }
        })

        // .catch(err => console.log(err));
        axios.post('http://localhost:5000/movie/moviesbycategory', {genre:"Action"})
        .then(result => {
          console.log(result);
          setGenre5(result.data)
            // console.log(result.data.message);
        })
        .catch(err => console.log(err));

        axios.post('http://localhost:5000/movie/moviesbycategory', {genre:"Mystery"})
        .then(result => {
          console.log(result);
          setGenre6(result.data)
            // console.log(result.data.message);
          
        })
        .catch(err => console.log(err));

        axios.post('http://localhost:5000/movie/moviesbycategory', {genre:"Animation"})
        .then(result => {
          console.log(result);
            setGenre7(result.data)
            // console.log(result.data.message);
        })
        .catch(err => console.log(err));

        axios.post('http://localhost:5000/movie/moviesbycategory', {genre:"Horror"})
        .then(result => {
          console.log(result);
          setGenre8(result.data)
            // console.log(result.data.message);
          
        })
        .catch(err => console.log(err));


        axios.post('http://localhost:5000/movie/moviesbycategory', {genre:"Romance"})
        .then(result => {
          console.log(result);
            setGenre9(result.data)
            // console.log(result.data.message);
          
        })
        .catch(err => console.log(err));

        axios.post('http://localhost:5000/movie/moviesbycategory', {genre:"Fantasy"})
        .then(result => {
          console.log(result);
            setGenre10(result.data)
            // console.log(result.data.message);
        })
        .catch(err => console.log(err));
     

  }, []);

  


  useEffect(() => {
    const swiper = new Swiper('.swiper-container', {
      direction: 'horizontal', 
      slidesPerView: 2,
      slidesPerGroup: 1,
      centeredSlides: true,
      loop: true,
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      breakpoints: {
        600: {
          slidesPerView: 2,
          slidesPerGroup: 2,
          spaceBetween: 5,
          centeredSlides: true,
        },
        900: {
          slidesPerView: 3,
          slidesPerGroup: 3,
          spaceBetween: 5,
          centeredSlides: false,
        },
        1200: {
          slidesPerView: 4,
          slidesPerGroup: 4,
          spaceBetween: 5,
          centeredSlides: false,
        },
        1500: {
          slidesPerView: 5,
          slidesPerGroup: 5,
          spaceBetween: 5,
          centeredSlides: false,
        },
        1800: {
          slidesPerView: 6,
          slidesPerGroup: 6,
          spaceBetween: 5,
          centeredSlides: false,
        },
      },
    });
  }, []);

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
    const encodedQuery = encodeURIComponent(searchQuery);
    navigate(`/search?query=${encodedQuery}`);

    console.log('Searching for:', searchQuery);
  };
  const [muted, setMuted] = useState(false);

  const toggleMute = () => {
    const video = videoRef.current;
    if (video) {
      video.muted = !video.muted;
      setMuted(!video.muted);
    }
  };
  const [seen1, setSeen1] = useState(false)

  function togglePop1 () {
      // setSelectedImage1(imageName)
      setSeen1(!seen1);
  };
  const handleClose1 = () => {
    setSeen1(false);
  };

  const [seen, setSeen] = useState(false)

  function togglePop (imageName) {
      setSelectedImage(imageName)
      setSeen(!seen);
  };
  const handleClose = () => {
    setSeen(false);
  };

  const imageList = [
    { name: 'Image 1', src: 'https://image.tmdb.org/t/p/w500/ba7hnMx1HAze0QSJSNfsTBycS8U.jpg' },
    { name: 'Image 2', src: 'https://image.tmdb.org/t/p/w500/c3XBgBLzB9Sh7k7ewXY2QpfH47L.jpg' },
    { name: 'Image 3', src: 'https://image.tmdb.org/t/p/w500/b5rOkbQ0jKYvBqBf3bwJ6nXBOtx.jpg' },
    { name: 'Image 4', src: 'https://image.tmdb.org/t/p/w500/aNsrgElf0fiKBSR8cWWEL6XUTte.jpg' },
    { name: 'Image 5', src: 'https://image.tmdb.org/t/p/w500/dueiWzWc81UAgnbDAyH4Gjqnh4n.jpg' },
    { name: 'Image 6', src: 'https://image.tmdb.org/t/p/w500/hwNRc9ZWrakGdql22srY7DqtmRQ.jpg' },
    { name: 'Image 7', src: 'https://image.tmdb.org/t/p/w500/trAOGwksvgHYNpbK4GewbjYQ1pi.jpg' },
    { name: 'Image 8', src: 'https://image.tmdb.org/t/p/w500/zAIippNnm6o0gYEtjapbjQSxP8G.jpg' },
    { name: 'Image 9', src: 'https://image.tmdb.org/t/p/w500/tNyJxHK3m7NAAKNYITLJ5oxS0YR.jpg' },
    { name: 'Image 10', src: 'https://image.tmdb.org/t/p/w500/hMh1mR2kNl8kHjpIuPh4TICTwjo.jpg' },
    { name: 'Image 11', src: 'https://image.tmdb.org/t/p/w500/c4EkF5JAZ83bUqNErhuSd9xw6uJ.jpg' },
    { name: 'Image 12', src: 'https://image.tmdb.org/t/p/w500/79DgItjsyH5tpA3mC2xv5gU2zlZ.jpg' }
  ];


  return (
    <div className="mainn">
      <Navbar
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
                {/* <Nav.Link as={Link} to="/search?query=${encodeURIComponent(searchQuery)}" onClick={() => updateExpanded(false)}> */}
                  <button className="search-button"  onClick={() => togglePop1()}  >
                    Search
                  </button>
                {/* </Nav.Link> */}
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
      
      <div>
        <div className="movie">
        
          <video ref={videoRef} autoPlay loop muted>
            <source src={videoSource} type="video/mp4" />
            Your browser does not support the video tag.
            
          </video>
          {/* <button  className='muteBtn' onClick={toggleMute}>{muted ? 'Unmute' : 'Mute'}</button> */}
          <button  className='muteBtn'style={{border: "none"}} onClick={toggleMute}>{muted ? <h3><i className="bi bi-volume-up"></i></h3> : <h3> <i className="bi bi-volume-mute"></i></h3>}</button>
          
          
        </div>
        {/* 1 */}
        <div className="container1-fluid"  style={{ paddingTop: '20px' }}>
          <p color='white'>Recommendations</p>
          <div className="swiper-container">
            <div className="swiper-wrapper">
              {imageList.map((image, index) => (
                <div key={index} className="swiper-slide">
                  
                <button style={{ backgroundColor: 'transparent',  border: 'none', padding: 0, margin: 0,}} onClick={() => togglePop(image.name)}>
                    <img src={image.src} alt={image.name} />
                  </button>
                </div>
              ))}
            </div>
             {/* <div className="swiper-button-next"></div>
            <div className="swiper-button-prev"></div>  */}
          </div>
        </div>


            {/* 2 */}

        <div className="container1-fluid " style={{ paddingTop: '50px' }}>
          <p color='white'>Recommendation based on Last Watched</p>
          <div className="swiper-container">
            <div className="swiper-wrapper">
              {imageList.map((image, index) => (
                <div key={index} className="swiper-slide">
                  
                <button style={{ backgroundColor: 'transparent',  border: 'none', padding: 0, margin: 0,}} onClick={() => togglePop(image.name)}>
                    <img src={image.src} alt={image.name} />
                  </button>
              
                </div>
              ))}
            </div>
            {/* <div className="swiper-button-next"></div>
            <div className="swiper-button-prev"></div> */}
          </div>
        </div>

        {/* 3------ */}

        <div className="container1-fluid " style={{ paddingTop: '50px' }}>
          <p color='white'>Top Rated</p>
          <div className="swiper-container">
            <div className="swiper-wrapper">
              {Genre3.map((image, index) => (
                <div key={index} className="swiper-slide">
                  
                <button style={{ backgroundColor: 'transparent',  border: 'none', padding: 0, margin: 0,}} onClick={() => togglePop(image.name)}>
                    <img src={image.src} alt={image.name} />
                  </button>
              
                </div>
              ))}
            </div>
            {/* <div className="swiper-button-next"></div>
            <div className="swiper-button-prev"></div> */}
          </div>
        </div>



             {/* 4------ */}
        <div className="container1-fluid " style={{ paddingTop: '50px' }}>
          <p color='white'>Crime</p>
          <div className="swiper-container">
            <div className="swiper-wrapper">
              {Genre4.map((image, index) => (
                <div key={index} className="swiper-slide">
                  
                <button style={{ backgroundColor: 'transparent',  border: 'none', padding: 0, margin: 0,}} onClick={() => togglePop(image.name)}>
                    <img src={image.src} alt={image.name} />
                  </button>
              
                </div>
              ))}
            </div>
            {/* <div className="swiper-button-next"></div>
            <div className="swiper-button-prev"></div> */}
          </div>
        </div>


             {/* 5------ */}

        <div className="container1-fluid " style={{ paddingTop: '50px' }}>
          <p color='white'>Action</p>
          <div className="swiper-container">
            <div className="swiper-wrapper">
              {Genre5.map((image, index) => (
                <div key={index} className="swiper-slide">
                  
                <button style={{ backgroundColor: 'transparent',  border: 'none', padding: 0, margin: 0,}} onClick={() => togglePop(image.name)}>
                    <img src={image.src} alt={image.name} />
                  </button>
              
                </div>
              ))}
            </div>
            {/* <div className="swiper-button-next"></div>
            <div className="swiper-button-prev"></div> */}
          </div>
        </div>



             {/* 6------ */}

        <div className="container1-fluid " style={{ paddingTop: '50px' }}>
          <p color='white'>Mystery</p>
          <div className="swiper-container">
            <div className="swiper-wrapper">
              {Genre6.map((image, index) => (
                <div key={index} className="swiper-slide">
                  
                <button style={{ backgroundColor: 'transparent',  border: 'none', padding: 0, margin: 0,}} onClick={() => togglePop(image.name)}>
                    <img src={image.src} alt={image.name} />
                  </button>
              
                </div>
              ))}
            </div>
            {/* <div className="swiper-button-next"></div>
            <div className="swiper-button-prev"></div> */}
          </div>
        </div>

             {/* 7------ */}

        <div className="container1-fluid " style={{ paddingTop: '50px' }}>
          <p color='white'>Animation</p>
          <div className="swiper-container">
            <div className="swiper-wrapper">
              {Genre7.map((image, index) => (
                <div key={index} className="swiper-slide">
                  
                <button style={{ backgroundColor: 'transparent',  border: 'none', padding: 0, margin: 0,}} onClick={() => togglePop(image.name)}>
                    <img src={image.src} alt={image.name} />
                  </button>
              
                </div>
              ))}
            </div>
            {/* <div className="swiper-button-next"></div>
            <div className="swiper-button-prev"></div> */}
          </div>
        </div>

             {/* 8------ */}

        <div className="container1-fluid " style={{ paddingTop: '50px' }}>
          <p color='white'>Horror</p>
          <div className="swiper-container">
            <div className="swiper-wrapper">
              {Genre8.map((image, index) => (
                <div key={index} className="swiper-slide">
                  
                <button style={{ backgroundColor: 'transparent',  border: 'none', padding: 0, margin: 0,}} onClick={() => togglePop(image.name)}>
                    <img src={image.src} alt={image.name} />
                  </button>
              
                </div>
              ))}
            </div>
            {/* <div className="swiper-button-next"></div>
            <div className="swiper-button-prev"></div> */}
          </div>
        </div>

             {/* 9------ */}


        <div className="container1-fluid " style={{ paddingTop: '50px' }}>
          <p color='white'>Romance</p>
          <div className="swiper-container">
            <div className="swiper-wrapper">
              {Genre9.map((image, index) => (
                <div key={index} className="swiper-slide">
                  
                <button style={{ backgroundColor: 'transparent',  border: 'none', padding: 0, margin: 0,}} onClick={() => togglePop(image.name)}>
                    <img src={image.src} alt={image.name} />
                  </button>
              
                </div>
              ))}
            </div>
            {/* <div className="swiper-button-next"></div>
            <div className="swiper-button-prev"></div> */}
          </div>
        </div>

             {/* 10------ */}

        <div className="container1-fluid " style={{ paddingTop: '50px' }}>
          <p color='white'>Fantasy</p>
          <div className="swiper-container">
            <div className="swiper-wrapper">
              {Genre10.map((image, index) => (
                <div key={index} className="swiper-slide">
                  
                <button style={{ backgroundColor: 'transparent',  border: 'none', padding: 0, margin: 0,}} onClick={() => togglePop(image.name)}>
                    <img src={image.src} alt={image.name} />
                  </button>
              
                </div>
              ))}
            </div>
            {/* <div className="swiper-button-next"></div>
            <div className="swiper-button-prev"></div> */}
          </div>
        </div>





        {seen && <MiniPage MovieId={selectedImage} onClose={handleClose} />}
       { console.log(seen1)}
        {seen1 && <SearchPage title={searchQuery} onClose={handleClose1}/>}
      </div> 
    </div> 
  );
}
