import React from "react";

import Loading from "@shared/ui/Loadind/Loading";

import styles from "./Position.module.scss";

interface PositionProps {
  position: number;
}

const Position: React.FC<PositionProps> = ({ position }) => {
  return (
    <div className={styles.position}>
      <div>position: {position}</div>
    </div>
  );
};

export default Position;
