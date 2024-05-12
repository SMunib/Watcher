import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import axios from 'axios';

export default function init_movie() {
    // const location = useLocation();
    // const selectedGenres = location.state.selectedGenres;
    const [movies, setAllMovies ]=useState([]);
    const [selectedMovies, setSelectedMovies] = useState([]);
    const navigate = useNavigate();
    useEffect(() => {
        // GET request to fetch movies when the component mounts
        axios.get('http://localhost:5000/api/movies')
            .then(response => {
                setAllMovies(response.data);
            })
            .catch(error => {
                console.error('Error fetching movies:', error);
            });
    }, []); 
    
    const moviess = [
        "The Shawshank Redemption",
        "The Godfather",
        "The Dark Knight",
        "Schindler's List",
        "Pulp Fiction",
        "Forrest Gump",
        "The Lord of the Rings: The Return of the King",
        "Fight Club",
        "Inception"
    ];
    const groupedMoviess = moviess.reduce((acc, curr, index) => {
        if (index % 3 === 0) {
            acc.push([curr]);
        } else {
            acc[acc.length - 1].push(curr);
        }
        return acc;
    }, []);

    const handleMovieClick = (movie) => {
        setSelectedMovies((prevSelectedMovies) => {
            if (prevSelectedMovies.includes(movie)) {
                // If the movie is already selected, remove it from the list
                return prevSelectedMovies.filter((selectedMovie) => selectedMovie !== movie);
            } else {
                // If the movie is not selected, add it to the list
                return [...prevSelectedMovies, movie];
            }
        });
    };

    const handleNextClick = () => {
        console.log('Selected movies for next:', selectedMovies);

             axios.post('http://localhost:5000/api/selectedMovies', { selectedMovies })
            .then(result => {
                console.log(result);    
                if (result.data.status === 200) {
                    navigate('/home');
                } else {
                    alert(result.data.message);
                }
            })
            .catch(err => console.log(err));

        navigate('/home');
        // Add logic to navigate to the next page or perform any other action
    };

    return (
        <div className='main'>
            <div className='imgDiv'></div>
            <div className='in'>
                <div className='select'>
                    Please select your favorite movies
                </div>
                {groupedMoviess.map((row, rowIndex) => (
                    <div key={rowIndex} className='row'>
                        {row.map((movie, colIndex) => (
                            <div
                                key={colIndex}
                                className={`column ${selectedMovies.includes(movie) ? 'selected' : ''}`}
                                onClick={() => handleMovieClick(movie)}
                            >
                                {movie}
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
    );
}
