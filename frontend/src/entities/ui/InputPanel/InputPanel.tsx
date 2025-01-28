import React, { useState, useEffect, useRef } from "react";

import styles from "./InputPanel.module.scss";
import { addUrlAsync } from "@app/redux/mainVideo/asyncAction";
import { useAppDispatch } from "@app/redux/store";

import { addUrl } from "@app/api/addUrl";
import { isValidYouTubeUrl } from "@feature/hooks/isValidYouTubeUrl";
import Input from "@shared/ui/Input/Input";
import Button from "@shared/ui/Button/Button";

const InputPanel: React.FC = () => {
  const [inputValue, setInputValue] = useState<string>("");
  const [wsStatus, setWsStatus] = useState<string[]>([]);
  const socketRef = useRef<WebSocket | null>(null);

  const dispatch = useAppDispatch();

  useEffect(() => {
    // Очистка при размонтировании компонента
    return () => {
      socketRef.current?.close();
    };
  }, []);

  const handleInputChange = (value: string) => {
    setInputValue(value);
  };

  const handleButtonClick = async () => {
    if (!isValidYouTubeUrl(inputValue)) {
      alert("Некорректная ссылка YouTube");
      return;
    }

    try {
      // const response = await addUrl(inputValue);

      const response = await dispatch(addUrlAsync(inputValue)).unwrap();
      console.log("Ответ от сервера:", response);
      console.log("start ws");
      openWebSocket();
    } catch (error) {
      console.error(error);
    }
  };

  const openWebSocket = () => {
    socketRef.current = new WebSocket(import.meta.env.WS_APP_API_URL);

    socketRef.current.onmessage = (event) => {
      setWsStatus((prevData) => [...prevData, event.data]);
      console.log("Message from server:", event.data);
    };

    socketRef.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  };

  return (
    <div className={styles.inputPanel}>
      <Input className={styles.input} onInputChange={handleInputChange} />
      <Button className={styles.button} onClick={handleButtonClick} />
    </div>
  );
};

export default InputPanel;
