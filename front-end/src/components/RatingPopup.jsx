import React, { useState } from 'react';

export default function RatingPopup({ onClose, onSubmit }) {
  const [rating, setRating] = useState('');

  const handleChange = (event) => {
    setRating(event.target.value);
  };

  const handleSubmit = () => {
    if (rating !== '') {
      const parsedRating = parseFloat(rating);
      if (parsedRating <= 10) {
        onSubmit(parsedRating);
        onClose();
      } else {
        alert('Rating should not exceed 10!');
      }
    } else {
      alert('Please enter a rating!');
    }
  };

  return (
    <div className="modal-overlay">
      <div className="popup2">
        <div className="popup-inner rating-popup2">
          <button onClick={onClose} type='button' className="btn-close btn-close-white" aria-label="Close"></button>
          <h2 className="text-white">Rate Movie</h2>
          <input
            type="number"
            step="0.1"
            min="0"
            max="10"
            placeholder="Enter rating"
            value={rating}
            onChange={handleChange}
          />
          <button onClick={handleSubmit} className="btn btn-primary">Submit</button>
        </div>
      </div>
    </div>
  );
}
