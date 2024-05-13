import React from 'react';
import { Button } from 'react-bootstrap';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';


export default function priority() {
//   const moviess = [
//     "The Shawshank Redemption",
//     "The Godfather",
//     "The Dark Knight",
//     "Schindler's List",
//     "Pulp Fiction",
//     "Forrest Gump",
//     "The Lord of the Rings: The Return of the King",
//     "Fight Club",
//     "Inception"
// ];
    const [genress, setGenres] = useState([]);
    const [genres, setSelectedGenres] = useState([]);
    const navigate = useNavigate();
    useEffect(() => {
      axios.get('http://localhost:5000/genres/select')
        .then(response => {
          setGenres(response.data);
        })
        .catch(error => {
          console.error('Error fetching genres:', error);
        });
    }, []);
            // Split genres into groups of 4
        const groupedGenres = genress.reduce((acc, curr, index) => {
            if (index % 4 === 0) {
            acc.push([curr]);
            } else {
            acc[acc.length - 1].push(curr);
            }
            return acc;
        }, []);
 
        const handleGenreClick = (genre) => {
            setSelectedGenres((prevSelectedGenres) => {
              const newSelectedGenres = [...prevSelectedGenres, genre];
              if (newSelectedGenres.length > 3) {
                newSelectedGenres.shift();
              }
              return newSelectedGenres;
            });
          };
          const [moviess, setMovies] = useState([]);
          const handleNextClick = () => {
            console.log('Selected genres for next:', genres);

            axios.post('http://localhost:5000/genres/select',{genres})
            .then(result=>{console.log(result)
            if( result.data.status === 200){
              console.log(result.data.status)
              console.log(result.data.movies)
              console.log(result.data.movies.title)
              setMovies(result.data.movies);
              navigate('/init_movie', { state: { movies: moviess } });
            }
            else{
              alert(result.data.message);
            }
          }
          )
            .catch(err=> console.log(err)) 
            // navigate('/init_movie');
           
            };
          // const handleskip = () => {
          //   navigate('/home');
          // };
      
  return (
    <div className='main'>
    
        <div className='imgDiv'></div>
        <div className='in'>
          <div className='select'>
          Please select your 3 favorite genres
          </div>
            {groupedGenres.map((row, rowIndex) => (
            <div key={rowIndex} className='row'>
                {row.map((genre, colIndex) => (
                 <div
                 key={colIndex}
                 className={`column ${genres.includes(genre) ? 'selected' : ''}`}
                 onClick={() => handleGenreClick(genre)}
               >
                 {genre}
               </div>
                ))}
            </div>
            ))}
       
                <div className='row1'>
                    <Button variant="primary" type="submit" className="btn-oval mx-3 mb-3" onClick={handleNextClick}>
                        Next
                    </Button>
                    <Link to="/home" className="skiplink mt-3 mb-2" >
                      Click here to skip
                    </Link>
                    
                </div>
              

        </div>    
       

          
    </div>
        
  )
}
