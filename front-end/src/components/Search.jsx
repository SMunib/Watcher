import React,{useEffect,useState} from 'react';
import Swiper from 'swiper';
import 'swiper/swiper-bundle.css';
import MiniPage from './minipage';

const SearchPage = ({query,onClose}) => {
  const [selectedImage, setSelectedImage] = useState(null);


useEffect(()=>{
  axios.post('http://localhost:5000/api/search', {query})
        .then(result => {
          console.log(result);
          if (result.data.status === 200) {
            console.log(result.data.message);
          } else {
            alert(result.data.message);
          }
        })

},[]);
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
  
    <div className="popup">
        <div className="popup-inner" style={{width:"100%"}}>
          <div className='main-1'>
          
          <div className="container1-fluid " style={{ paddingTop: '50px' }}>
          <p color='white'>Search Result</p>
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
          <button onClick={onClose} type='button' className="btn-close btn-close-white" aria-label="Close" style={{paddingRight: "50px"}}></button>
        </div>
            
           
          </div>
      
          <div className='contentDiv text-white pt-4'>
            <div className='left_content'>
            
            </div>
            <div className='right_content'>
         
            </div>
          </div>
        </div>
            {console.log(query)}
            {seen && <MiniPage movieName={selectedImage} onClose={handleClose} />}
      </div>
      
  );
}
export default SearchPage;