import './App.css';
import MobileCam from './components/MobileCam';
import LaptopView from './components/LaptopView';

function App() {
  const isMobile = /Mobi|Android/i.test(navigator.userAgent);

  return (
    <div className="App">
      <h1>Real-Time Object Tracker</h1>
      {isMobile ? (
        <>
          <p>📱 Mobile Mode: Sending camera feed...</p>
          <MobileCam />
        </>
      ) : (
        <>
          <p>💻 Laptop Mode: Receiving and interacting with feed...</p>
          <LaptopView />
        </>
      )}
    </div>
  );
}

export default App;
