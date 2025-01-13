import styles from "./InputPanel.module.scss";

import Input from "@shared/ui/Input/Input";
import Button from "@shared/ui/Button/Button";

const InputPanel = () => {
  return (
    <div className={styles.inputPanel}>
      <Input className={styles.input} />
      <Button className={styles.button} />
    </div>
  );
};

export default InputPanel;
