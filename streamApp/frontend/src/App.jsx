import React, { useState } from "react";
import MobileCam from "./components/MobileCam";
import LaptopView from "./components/LaptopView";

export default function App() {
  const [role, setRole] = useState(null);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      {!role ? (
        <>
          <h1>Select Your Device</h1>
          <button
            onClick={() => setRole("mobile")}
            style={{ margin: "10px", padding: "10px 20px" }}
          >
            Use as Mobile
          </button>
          <button
            onClick={() => setRole("laptop")}
            style={{ margin: "10px", padding: "10px 20px" }}
          >
            Use as Laptop
          </button>
        </>
      ) : role === "mobile" ? (
        <MobileCam />
      ) : (
        <LaptopView />
      )}
    </div>
  );
}