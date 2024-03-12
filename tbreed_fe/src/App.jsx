import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import Home from "./Pages/Home" // a few buttons to activate - download, embed sentences, launch clustering
import Visualize from "./Pages/Visualize"
import {BrowserRouter as Router, Routes, Route, Link} from "react-router-dom";
import './App.css';
import React from "react";

function App() {
  return (
    <Router>
      <div>
        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/visualize" element={<Visualize />} />
            


        </Routes>
      </div>
    </Router>
  )
}

export default App
