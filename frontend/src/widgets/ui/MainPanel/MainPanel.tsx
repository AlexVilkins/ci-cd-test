import React, { useState, useEffect, useRef } from "react";

import styles from "./MainPanel.module.scss";
import InputPanel from "@entities/ui/InputPanel/InputPanel";
import LoadingBar from "@shared/ui/LoadingBar/LoadingBar";
import { useAppDispatch } from "@app/redux/store";
import { isValidYouTubeUrl } from "@feature/hooks/isValidYouTubeUrl";
import { addUrlAsync } from "@app/redux/mainVideo/asyncAction";
import {
  setPanelType,
  setButtonDesable,
  dropeState,
  setPosition,
} from "@app/redux/mainVideo/slice";
import { useAppSelector } from "@app/redux/store";

const MainPanel: React.FC = () => {
  const [progress, setProgress] = useState(0);
  const [inputValue, setInputValue] = useState<string>("");

  const socketRef = useRef<WebSocket | null>(null);
  const dispatch = useAppDispatch();

  const { panelType, position } = useAppSelector(
    (state) => state.mainVideoSlice
  );

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
    console.log("click");
    if (!isValidYouTubeUrl(inputValue)) {
      alert("Некорректная ссылка YouTube");
      return;
    }

    try {
      dispatch(setButtonDesable({ desableButton: true }));
      dispatch(setPanelType({ panelType: "loading", img_url: "" }));
      const response = await dispatch(addUrlAsync(inputValue)).unwrap();
      console.log("Ответ от сервера:", response);
      console.log("port", response.port);

      console.log("start ws");
      // dispatch(setPanelType("img"));
      openWebSocket(response.port);
    } catch (error) {
      console.error(error);
      dispatch(setButtonDesable({ desableButton: false }));
    }
  };

  const openWebSocket = (port: string) => {
    socketRef.current = new WebSocket(
      `${import.meta.env.VITE_WS_APP_API_URL}/${port}`
    );

    console.log(
      "WebSocket port:",
      `${import.meta.env.VITE_WS_APP_API_URL}/${port}`
    );
    socketRef.current.onmessage = (event) => {
      console.log("Message from server:", JSON.parse(event.data));
      if (JSON.parse(event.data).type_mess === "queue_position") {
        dispatch(
          setPosition({
            position: JSON.parse(event.data).text,
          })
        );
      }

      if (JSON.parse(event.data).type_mess === "progress") {
        setProgress((data) => {
          if (data < JSON.parse(event.data).text)
            return JSON.parse(event.data).text;
        });
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
      dispatch(setButtonDesable({ desableButton: false }));
      setProgress(0);
    };

    socketRef.current.onerror = (error) => {
      console.error("WebSocket error:", error);

      dispatch(dropeState());
    };
  };

  return (
    <div className={styles.mainPanel}>
      <InputPanel
        handleInputChange={handleInputChange}
        handleButtonClick={handleButtonClick}
      />
      <LoadingBar
        progress={progress}
        panelType={panelType}
        position={position}
      />
    </div>
  );
};

export default MainPanel;
