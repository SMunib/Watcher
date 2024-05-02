import React from 'react';
import { Button } from 'react-bootstrap';
import axios from 'axios';
import { FiLogIn } from 'react-icons/fi';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';


export default function priority() {
    const [genres, setGenres] = useState([]);
    const [selectedGenres, setSelectedGenres] = useState([]);
    const navigate = useNavigate();
    useEffect(() => {
      axios.get('http://localhost:5000/api/select')
        .then(response => {
          setGenres(response.data);
        })
        .catch(error => {
          console.error('Error fetching genres:', error);
        });
    }, []);
      

    const genress = [
        'Telescene Film Group Productions',
        'War',
        'Mystery',
        'Carousel Productions',
        'BROSTA TV',
        'Drama',
        'Adventure',
        'Romance',
        'Action',
        'Documentary',
        'Thriller',
        'Western',
        'Fantasy',
        'Sentai Filmworks',
        'Horror',
        'TV Movie',
        'Mardock Scramble Production Committee',
        'Vision View Entertainment',
        'The Cartel',
        'Animation',
        'Pulser Productions',
        'Science Fiction',
        'History',
        'Family',
        'Crime',
        'Rogue State',
        'Comedy',
        'Aniplex',
        'Odyssey Media',
        'Foreign',
        'GoHands',
        'Music'
      ];
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
          
          const handleNextClick = () => {
            console.log('Selected genres for next:', selectedGenres);
            navigate('/init_movie');
            axios.post('http://localhost:5000/api/genres',{selectedGenres})
            .then(result=>{
              console.log(result)
              if(result.data.status === 200){
                navigate('/init_movie');
              }
                else {
                  // Show error message if email or password is incorrect
                  
                  alert(result.data.message);
                }
                })
                .catch(err=> console.log(err))
                
            };
      
  return (
    <div className='main'>
        <div className='imgDiv'></div>
        <div className='in'>
            {groupedGenres.map((row, rowIndex) => (
            <div key={rowIndex} className='row'>
                {row.map((genre, colIndex) => (
                 <div
                 key={colIndex}
                 className={`column ${selectedGenres.includes(genre) ? 'selected' : ''}`}
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
                </div>
        </div>        
    </div>
        
  )
}
