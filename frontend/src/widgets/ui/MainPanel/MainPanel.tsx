import React, { useState, useEffect } from "react";

import styles from "./MainPanel.module.scss";
import InputPanel from "@entities/ui/InputPanel/InputPanel";
import LoadingBar from "@shared/ui/LoadingBar/LoadingBar";

const MainPanel = () => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10; // Увеличиваем прогресс на 10% каждые 500 мс
      });
    }, 500);

    return () => clearInterval(interval); // Очистка интервала при размонтировании
  }, []);

  return (
    <div className={styles.mainPanel}>
      <InputPanel />
      <LoadingBar progress={progress} />
    </div>
  );
};

export default MainPanel;
