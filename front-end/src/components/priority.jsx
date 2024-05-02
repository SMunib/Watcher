import React from 'react';
import { Button } from 'react-bootstrap';
import { FiLogIn } from 'react-icons/fi';
export default function priority() {
    const [genres, setGenres] = useState([]);
    const [selectedGenres, setSelectedGenres] = useState([]);

    useEffect(() => {
      axios.get('http://localhost:5000/genres')
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
            // Add your logic here to navigate to the next page or perform any other action
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
