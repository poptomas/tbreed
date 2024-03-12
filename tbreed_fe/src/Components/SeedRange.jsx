import React, { useState } from 'react';

const SeedRange = () => {
    const [seedRange, setSeedRange] = useState(0);

  const handleRangeChange = (event) => {
    const newRange = parseInt(event.target.value);
    console.log(newRange);
    setSeedRange(newRange);
  };

  return (
    <div>
<input
        type="number"
        min="0"
        max="1000"
        onChange={handleRangeChange}
        id="seedInput"
        value={seedRange}
      />

    </div>
  );
};

export default SeedRange;