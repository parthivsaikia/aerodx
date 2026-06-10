function CTPreview({ image }) {
  return (
    <div
      style={{
        marginTop: "20px",
        border: "1px solid #ddd",
        borderRadius: "12px",
        padding: "20px",
      }}
    >
      <h2>CT Scan Preview</h2>

      <div
        style={{
          height: "250px",
          backgroundColor: "#f3f4f6",
          borderRadius: "10px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          overflow: "hidden",
        }}
      >
        {image ? (
          <img
            src={image}
            alt="CT Scan"
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
            }}
          />
        ) : (
          <p>No CT Scan Selected</p>
        )}
      </div>
    </div>
  );
}

export default CTPreview;