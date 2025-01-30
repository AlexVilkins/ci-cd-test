import React from "react";
import styles from "./LoadingBar.module.scss";

interface LoadingBarProps {
  progress: number; // Прогресс от 0 до 100
  panelType: "none" | "loading" | "img" | "video";
  position: number;
}

const LoadingBar: React.FC<LoadingBarProps> = ({
  progress,
  panelType,
  position,
}) => {
  return (
    <>
      {position > 1 && <div>position: {position}</div>}
      {panelType === "img" && position === 1 && (
        <div className={styles.loadingBar}>
          <div
            className={styles.progressBar}
            style={{
              width: `${progress}%`,
              backgroundColor: progress < 100 ? "#ffcc00" : "#4caf50",
            }}
          />
        </div>
      )}
    </>
  );
};

export default LoadingBar;
