import React, { useEffect, useState } from 'react';
import RatingPopup from './RatingPopup';
import axios from 'axios';

export default function MiniPage({ movieName, onClose }) {
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [showRatingPopup, setShowRatingPopup] = useState(false); // Ensure initial value is false
  
  useEffect(()=>{
    axios.post('http://localhost:5000/api/register',{movieName})
    .then(result=>{console.log(result)
    if( result.data.status === 200){
      console.log(result.data.message)
    }
    else{
      alert(result.data.message);
    }
  }
  )
    .catch(err=> console.log(err))  
  },[])

  const movie = {
    name: "Inception",
    picturePath: "https://image.tmdb.org/t/p/w500/79DgItjsyH5tpA3mC2xv5gU2zlZ.jpg",
    cast: ["Leonardo DiCaprio, ", "Joseph Gordon-Levitt, ", "Ellen Page"],
    director: "Christopher Nolan",
    imdbRating: 8.8,
    synopsis: "Inception is a science fiction action film written and directed by Christopher Nolan. The film stars Leonardo DiCaprio as a professional thief who steals information by infiltrating the subconscious of his targets.",
    add: "no"
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [onClose]);

  const handleAddButtonClick = () => {
    setSelectedMovie(movie.name);
    axios.post('http://localhost:5000/api/addToList', { selectedMovie })
            .then(result => {
                console.log(result);    
                if (result.data.status === 200) {
                  
                } else {
                    alert(result.data.message);
                }
            })
            .catch(err => console.log(err));
  };

  const handleRateButtonClick = () => {
    console.log("Rate button clicked"); // Debugging statement
    setShowRatingPopup(true);
  };

  const handleCloseRatingPopup = () => {
    setShowRatingPopup(false);
  };

  const handleRatingSubmit = (rating) => {
    // Handle rating submission here
    console.log("Rating submitted:", rating);

    axios.post('http://localhost:5000/api/rating', { selectedMovie,rating })
    .then(result => {
        console.log(result);    
        if (result.data.status === 200) {
          
        } else {
            alert(result.data.message);
        }
    })
    .catch(err => console.log(err));
    setShowRatingPopup(false);
  };

  return (
    <>
      <div className="popup">
        <div className="popup-inner">
          <div className='main-1'>
            <div className='moviepic' style={{backgroundImage: `linear-gradient(to bottom, transparent 70%, rgba(0, 0, 0, 0.7)), url(${movie.picturePath})`}}>
              <button onClick={onClose} type='button' className="btn-close btn-close-white" aria-label="Close" style={{top:"10px"}} ></button>
             <div className="rateWrapper">
                {movie.add === "no" && (
                  <button className='addbutton' onClick={handleAddButtonClick}>
                    {selectedMovie === movie.name ? <i className="bi bi-check-circle-fill"></i> : <i className="bi bi-plus-circle"></i>}
                  </button>
                )}
                <button onClick={handleRateButtonClick} type="button" className="btn btn-outline-secondary" style={{paddingLeft: "100px !important"}}>Rate</button>   
              </div>           
            </div>
          </div>
      
          <div className='contentDiv text-white pt-4'>
            <div className='left_content'>
              {movie.synopsis}
            </div>
            <div className='right_content'>
              <p>
                Cast: {movie.cast}
              </p>
              <p>Director: {movie.director}</p>
              <p>Imbd Rating: {movie.imdbRating}</p>
            </div>
          </div>
        </div>
        {showRatingPopup && <RatingPopup onClose={handleCloseRatingPopup} onSubmit={handleRatingSubmit} />}
      </div>
      
    </>
  );
}
