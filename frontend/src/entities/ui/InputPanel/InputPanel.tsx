import React from "react";

import Input from "@shared/ui/Input/Input";
import Button from "@shared/ui/Button/Button";

import styles from "./InputPanel.module.scss";

interface ButtonProps {
  handleButtonClick: () => void;
  handleInputChange: (value: string) => void;
}

const InputPanel: React.FC<ButtonProps> = ({
  handleButtonClick,
  handleInputChange,
}) => {
  return (
    <div className={styles.inputPanel}>
      <Input className={styles.input} onInputChange={handleInputChange} />
      <Button className={styles.button} onClick={handleButtonClick} />
    </div>
  );
};

export default InputPanel;
