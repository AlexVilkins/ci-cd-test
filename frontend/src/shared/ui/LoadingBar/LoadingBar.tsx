import React from "react";
import styles from "./LoadingBar.module.scss";

interface LoadingBarProps {
  progress: number; // Прогресс от 0 до 100
}

const LoadingBar: React.FC<LoadingBarProps> = ({ progress }) => {
  return (
    <div className={styles.loadingBar}>
      <div
        className={styles.progressBar}
        style={{
          width: `${progress}%`,
          backgroundColor: progress < 100 ? "#ffcc00" : "#4caf50",
        }}
      />
    </div>
  );
};

export default LoadingBar;
