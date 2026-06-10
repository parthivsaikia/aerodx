import { useState } from "react";
import Navbar from "./components/Navbar";
import UploadBox from "./components/UploadBox";
import CTPreview from "./components/CTPreview";
import ResultCard from "./components/ResultCard";
import ChatWindow from "./components/ChatWindow";

function App() {
  const [image, setImage] = useState(null);

  return (
    <>
      <Navbar />

      <div style={{ display: "flex", gap: "20px", padding: "20px" }}>
        <div style={{ flex: 1 }}>
          <UploadBox onImageUpload={setImage} />
          <CTPreview image={image} />
          <ResultCard />
        </div>

        <div style={{ flex: 1 }}>
          <ChatWindow />
        </div>
      </div>
    </>
  );
}

export default App;