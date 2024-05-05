// MiniPage.js
import React from 'react';
import { useParams } from 'react-router-dom';
export default function MiniPage() {
    let { movieName } = useParams();
  return (
    <div>
    <h2>{movieName}</h2>
    {/* Other content of the MiniPage */}
  </div>
  );
}
