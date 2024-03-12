import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

const Visualize = (props) => {
    const { number } = props;
    // Access the 'number' parameter from the route
    const [htmlContent, setHtmlContent] = useState('');
    useEffect(() => {
        const fetchData = async () => {
            console.log(number)
          try {
            // Fetch HTML content for the specified number
            const response = await fetch(`http://localhost:5000/cluster_visualization${number}.html`);
            const data = await response.text();
            setHtmlContent(data);
          } catch (error) {
            console.error('Error fetching HTML content:', error);
          }
        };
    
        fetchData();
      }, [number]);

      return (
        <div>
            <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
        </div>
      );
  };
  
  export default Visualize;