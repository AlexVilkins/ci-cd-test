import styles from "./MainPanel.module.scss";
import InputPanel from "@entities/ui/InputPanel/InputPanel";

const MainPanel = () => {
  return (
    <div className={styles.mainPanel}>
      <InputPanel />
    </div>
  );
};

export default MainPanel;
