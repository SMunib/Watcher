import React from 'react';
import { useLocation } from 'react-router-dom';

const SearchPage = ({query}) => {
// export default function SearchPage() {
//   const location = useLocation();
//   const queryParams = new URLSearchParams(location.search);
//   const query = queryParams.get('query');

  return (
    <div>
      <h1>Search Results for: {query}</h1>
      
      {/* Add search results or any other content here */}
    </div>
  );
}
export default SearchPage;