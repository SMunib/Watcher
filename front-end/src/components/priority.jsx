import React from 'react';
import { Button } from 'react-bootstrap';

export default function priority() {
  return (
    <div className='main'>
        <div className='imgDiv'></div>
        
            <div className='in'>
                <div className='row'>
                    <div className='column'>
                        A
                    </div>
                    <div className='column'>
                        A
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                    B
                    </div>
                    <div className='column'>
                    B
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        C
                    </div>
                    <div className='column'>
                        C
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        D
                    </div>
                    <div className='column'>
                        D
                    </div>
                </div>
           
            <div className='row1'>
            <Button variant="primary" type="submit" className="btn-oval mx-3 mb-3">
                     Next
                  </Button>
            </div>
        </div>
        




    </div>
  )
}
