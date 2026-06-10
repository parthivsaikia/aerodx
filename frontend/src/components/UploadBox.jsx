function UploadBox({ onImageUpload }) {
  const handleImageChange = (event) => {
    const file = event.target.files[0];
    console.log("File selected:", file);

    if (file) {
      const imageUrl = URL.createObjectURL(file);
      onImageUpload(imageUrl);
    }
  };

  return (
    <div
      style={{
        border: "2px dashed #ccc",
        padding: "30px",
        marginTop: "20px",
        borderRadius: "10px",
      }}
    >
      <h2>Upload CT Scan</h2>

      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
      />

      <br />
      <br />

      <button>Analyze Scan</button>
    </div>
  );
}

export default UploadBox;