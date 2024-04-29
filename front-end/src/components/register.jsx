import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import { FiLogIn } from 'react-icons/fi';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [username, setUsername] = useState('');
  const [passwordMatch, setPasswordMatch] = useState(true);
  const navigate = useNavigate();
  
  const handleSignIn = (e) => {
    e.preventDefault();
    if (password === confirmPassword) {
      setPasswordMatch(true);
    
      axios.post('http://localhost:5000/api/register',{username,email,password})
      .then(result=>{console.log(result)
      if( result.data.status === 200){
        console.log(result.data.message)
        navigate('/Login');
        
      }
      else{
        alert(result.data.message);
      }
    }
    )
      .catch(err=> console.log(err))   
    } else {
      // Passwords do not match, display error message
      setPasswordMatch(false);
    }
  };
  return (
    <div className='main'>
      <div className='imgDiv'>
      </div>
      <div className='content'>
        <Container>
          <Row className="justify-content-center align-items-center">
            <Col md={12} className='trans'>
              <h2 className='log1 mb-5 text-center'>Sign up </h2>
              <div className='mob1'>
                <Form onSubmit={handleSignIn}>
                  <Form.Group controlId="formBasicUsername" className='mb-4 mx-3'>
                    <Form.Control type="text" placeholder="Enter Username" value={username} onChange={(e) => setUsername(e.target.value)} required className='field1' />
                  </Form.Group>
                  <Form.Group controlId="formBasicEmail" className='mb-4 mx-3'>
                    <Form.Control type="email" placeholder="Enter email" value={email} onChange={(e) => setEmail(e.target.value)} required className='field1' />
                  </Form.Group>
                  <Form.Group controlId="formBasicPassword" className='mb-4 mx-3'>
                    <Form.Control type="password" placeholder="Enter password" value={password} onChange={(e) => setPassword(e.target.value)} required className='field1' />
                  </Form.Group>
                  <Form.Group controlId="formBasicConfirmPassword" className='mb-4 mx-3'>
                    <Form.Control type="password" placeholder="Retype password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required className='field1' />
                    {!passwordMatch && <Form.Text className="text-danger">Passwords do not match</Form.Text>}
                  </Form.Group>
                  <Button variant="primary" type="submit" className="btn-oval mx-3 mb-2">
                    <FiLogIn className='mx-1' /> Sign Up
                  </Button>
                  <Link to="/Login" className="btn-sm mt-3 mb-2" style={{ fontSize: '14px', color: 'white', paddingLeft: '20px' }}>
                    Already have an account? Sign In
                  </Link>
                </Form>
              </div>
            </Col>
          </Row>
        </Container>
      </div>
    </div>
  );
}
