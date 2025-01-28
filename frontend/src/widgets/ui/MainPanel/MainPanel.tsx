import React, { useState, useEffect, useRef } from "react";

import styles from "./MainPanel.module.scss";
import InputPanel from "@entities/ui/InputPanel/InputPanel";
import LoadingBar from "@shared/ui/LoadingBar/LoadingBar";
import { useAppDispatch } from "@app/redux/store";
import { isValidYouTubeUrl } from "@feature/hooks/isValidYouTubeUrl";
import { addUrlAsync } from "@app/redux/mainVideo/asyncAction";
import { setPanelType, setButtonDesable } from "@app/redux/mainVideo/slice";

const MainPanel = () => {
  const [progress, setProgress] = useState(0);
  const [inputValue, setInputValue] = useState<string>("");

  const socketRef = useRef<WebSocket | null>(null);
  const dispatch = useAppDispatch();

  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     setProgress((prev) => {
  //       if (prev >= 100) {
  //         clearInterval(interval);
  //         return 100;
  //       }
  //       return prev + 10; // Увеличиваем прогресс на 10% каждые 500 мс
  //     });
  //   }, 500);

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
      dispatch(setButtonDesable(true));
      const response = await dispatch(addUrlAsync(inputValue)).unwrap();
      console.log("Ответ от сервера:", response);
      console.log("start ws");
      // dispatch(setPanelType("img"));
      openWebSocket();
    } catch (error) {
      console.error(error);
      // TODO: Открыть конопку
    }
  };

  const openWebSocket = () => {
    socketRef.current = new WebSocket(import.meta.env.VITE_WS_APP_API_URL);

    socketRef.current.onmessage = (event) => {
      // setWsStatus((prevData) => [...prevData, event.data]);

      console.log("Message from server:", JSON.parse(event.data));

      if (JSON.parse(event.data).type_mess === "progress") {
        // TODO: тут проценты
        setProgress(JSON.parse(event.data).text);
      }
      if (JSON.parse(event.data).type_mess === "video_download") {
        dispatch(
          setPanelType({
            panelType: "video",
            img_url: JSON.parse(event.data).text,
          })
        );
      }
    };

    socketRef.current.onclose = (event) => {
      console.log("WebSocket closed:", event);
      // TODO: Открыть конопку
    };

    socketRef.current.onerror = (error) => {
      console.error("WebSocket error:", error);
      // TODO: Открыть конопку и сбросить стейты и сообщение об ошибке
    };
  };

  return (
    <div className={styles.mainPanel}>
      <InputPanel
        handleInputChange={handleInputChange}
        handleButtonClick={handleButtonClick}
      />
      <LoadingBar progress={progress} />
    </div>
  );
};

export default MainPanel;
