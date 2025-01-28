import React from "react";

import styles from "./Input.module.scss";

interface InputProps {
  onInputChange: (value: string) => void;
}

const Input: React.FC<InputProps> = ({ onInputChange }) => {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    onInputChange(value);
  };

  return (
    <input
      className={styles.input}
      placeholder="Введите ссылку видеоролика..."
      onChange={handleChange}
    />
  );
};

export default Input;
