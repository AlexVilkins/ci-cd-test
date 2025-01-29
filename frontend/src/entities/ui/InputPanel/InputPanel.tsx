import React, { useState, useEffect, useRef } from "react";

import Input from "@shared/ui/Input/Input";
import Button from "@shared/ui/Button/Button";

import styles from "./InputPanel.module.scss";

const InputPanel: React.FC<Button> = ({
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
