import styles from "./Input.module.scss";

const Input = () => {
  return (
    <input
      className={styles.input}
      placeholder="Введите ссылку видеоролика..."
    />
  );
};

export default Input;
