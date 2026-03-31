// App.tsx - Main application component

import React from "react";
import { Dashboard } from "./components/Dashboard";
import "./styles/globals.css";

export const App: React.FC = () => {
  return (
    <div className="App">
      <Dashboard />
    </div>
  );
};

export default App;