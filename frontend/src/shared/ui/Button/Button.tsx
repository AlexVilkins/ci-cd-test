import React from "react";

import { useAppSelector } from "@app/redux/store";

import styles from "./Button.module.scss";

interface InputProps {
  onClick: () => void;
}

const Button: React.FC<InputProps> = ({ onClick }) => {
  const { desableButton } = useAppSelector((state) => state.mainVideoSlice);

  return (
    <button
      className={styles.button}
      disabled={desableButton}
      onClick={() => onClick()}
    >
      Поиск
    </button>
  );
};

export default Button;
