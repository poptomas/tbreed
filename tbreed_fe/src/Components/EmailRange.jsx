import React, { useState } from 'react';

const EmailRange = () => {
    const [emailRange, setEmailRange] = useState(10000);

  const handleRangeChange = (event) => {
    const newRange = parseInt(event.target.value);
    console.log(newRange);
    setEmailRange(newRange);
  };

  return (
    <div>
<input
        type="number"
        min="100"
        max="500000"
        onChange={handleRangeChange}
        className="emailRangeInput"
        value={emailRange}
      />

    </div>
  );
};

export default EmailRange;