// MiniPage.js
import React, {useState} from 'react';
import { useParams } from 'react-router-dom';
export default function MiniPage({ movieName, onClose }) {
    // let { movieName } = useParams();

    const movie = {
      name: "Inception",
      picturePath: "https://image.tmdb.org/t/p/w500/79DgItjsyH5tpA3mC2xv5gU2zlZ.jpg",
      cast: ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
      director: "Christopher Nolan",
      imdbRating: 8.8,
      synopsis: "Inception is a science fiction action film written and directed by Christopher Nolan. The film stars Leonardo DiCaprio as a professional thief who steals information by infiltrating the subconscious of his targets."
    };
    

    
  return (
    <>
    
    <div className="popup">
      <div className="popup-inner">
        <div className='main-1'>
          <div className='moviepic' style={{backgroundImage:`url(${movie.picturePath})`}}></div>
          <h1 style={{color: "white"}}>{movieName}</h1>
        <button onClick={onClose} className="close-button">Close</button>
        </div>
        
      </div>
      
    </div>  
        </>
  );
}
