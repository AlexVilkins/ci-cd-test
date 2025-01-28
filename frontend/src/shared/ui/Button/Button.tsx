import React from "react";
import styles from "./Button.module.scss";

interface InputProps {
  onClick: () => void;
}

const Button: React.FC<InputProps> = ({ onClick }) => {
  return (
    <button className={styles.button} onClick={() => onClick()}>
      Поиск
    </button>
  );
};

export default Button;
