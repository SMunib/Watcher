import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import { FiLogIn } from 'react-icons/fi';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { setGlobalVariable } from './Global';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const[firstTime,setFirst]=useState('')
  const navigate = useNavigate();

const ema=['1@gmail.com'];
const pass=['1'];

const isEmailValid = ema.includes(email);
const isPasswordValid = pass.includes(password);

// useEffect(() => {
//   axios.get('http://localhost:5000/api/First')
//     .then(response => {
//       setFirst(response.data);
//     })
//     .catch(error => {
//       console.error('Error fetching genres:', error);
//     });
// }, []);

const [id,setId]=useState();
  const handleSignIn = (e) => {
    e.preventDefault(); // Prevent default form submission
    axios.post('http://localhost:5000/auth/login',{email,password})
    .then(result=>{
      console.log(result)
      if(result.data.status === 200){
        console.log(result.data.isFirstTime);
        setId(result.data.userid);
        console.log("hello");
        setGlobalVariable(result.data.userid);

        if(result.data.isFirstTime){
        navigate('/priority');
        }
        else{
          // navigate('/priority');
          navigate('/Home');
        }
      }
      else {
        // Show error message if email or password is incorrect
        // alert(result.data.message);
        alert("Email or Password is incorrect")
      }
    })
    .catch(err=> console.log(err))

    //  navigate('/priority');
  };

  return (
    <>
      <div className="app">
    
        <div className="left-pane">
            <div className='imgDiv'>
                
            </div>
          <div className="hh centered-content">
                <h2 className="welc text-center mb-3" style={{ color: 'white', fontWeight: 'bold' }}>Welcome</h2>
                {/* <p className="query text-center" style={{ color: 'red', fontWeight: 'bold' }}>This is a user authentication website designed for the purpose of
                implementing socket programming to authenticate user with the highest security possible
                </p> */}
          </div>
           <div>
           <p className="qu text-center">
                For any queries contact us at maam@gmail.com
                </p>
           </div>
        </div>
        <div className="right-pane">
        <Container>
            <Row className="justify-content-center align-items-center">
              <Col md={6} className='trans'>
                <h2 className='log mb-5 text-center'>Sign in </h2>
                {/* <p className='mini text-center mb-3' style={{ fontSize: '11px' }}>
                  Lorem ipsum dolor sit amet, consectetur adipisicing elit. Facilis fuga ad aspernatur aut aliquam ratione, illo ullam qui
                </p> */}
                <div className='mob'>
                  <Form onSubmit={handleSignIn}>
                    <Form.Group controlId="formBasicEmail " className=' mb-4 mx-3'>
                      {/* <Form.Label className='cred mx-2 text-center'>Email address</Form.Label> */}
                      <Form.Control type="email" placeholder="Enter email" value={email} onChange={(e) => setEmail(e.target.value)} required className='field' />
                    </Form.Group>

                    <Form.Group controlId="formBasicPassword" className=' mb-4 mx-3'>
                      {/* <Form.Label className='cred mx-2 text-center'>Password</Form.Label> */}
                      <Form.Control type="password" placeholder="Enter password" value={password} onChange={(e) => setPassword(e.target.value)} required className='field' />
                    </Form.Group>

                    <Button variant="primary" type="submit" className="btn-oval mx-3 mb-2">
                      <FiLogIn className='mx-1' /> Sign In
                    </Button>

                    <Link to="/Register" className="btn-sm mt-3 mb-2" style={{ fontSize: '14px', color: 'white', paddingLeft: '20px',  }}>
                      Don't have an account yet?
                      
                    </Link>

                  </Form>
                </div>
              </Col>
            </Row>
          </Container>
        </div>
      </div>
    </>
  );
}

export default Login;
