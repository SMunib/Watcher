import './Style.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/login';   
import Register from './components/register';
import Priority from './components/priority';
import Init_movie from './components/init_movie';
import Home from './components/home';
import MiniPage from './components/minipage';

function App() {


  return (
    <>
     <Router>
     
      <Routes>
        <Route  path="/" element={<Login />}  />
        <Route  path="/Register"  element={<Register />} />        
        <Route  path="/Priority"  element={<Priority />} />
        <Route  path="/init_movie"  element={<Init_movie />} />
        <Route  path="/Home"  element={<Home />} />  
        <Route  path="/Login" element={<Login />}  />     
        <Route path="/minipage/:movieName" element={<MiniPage />} />
      </Routes> 
    </Router>     
    </>
  )
}

export default App
