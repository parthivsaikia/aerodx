function ResultCard() {
  return (
    <div
      style={{
        marginTop: "20px",
        padding: "20px",
        border: "1px solid #ddd",
        borderRadius: "12px",
      }}
    >
      <h2>Prediction Result</h2>

      <p>
        <strong>Disease:</strong> Pneumonia
      </p>

      <p>
        <strong>Confidence:</strong> 94%
      </p>

      <div
        style={{
          backgroundColor: "#e5e7eb",
          height: "12px",
          borderRadius: "10px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: "94%",
            height: "100%",
            backgroundColor: "#22c55e",
          }}
        />
      </div>
    </div>
  );
}

export default ResultCard;