import React from "react";

import useFocus from "@feature/hooks/useFocus";
import styles from "./Input.module.scss";

interface InputProps {
  onInputChange: (value: string) => void;
}

const Input: React.FC<InputProps> = ({ onInputChange }) => {
  const inputRef = useFocus();
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    onInputChange(value);
  };

  return (
    <input
      ref={inputRef}
      className={styles.input}
      placeholder="Введите ссылку видеоролика..."
      onChange={handleChange}
    />
  );
};

export default Input;
