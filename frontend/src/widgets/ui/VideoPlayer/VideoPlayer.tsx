import styles from "./VideoPlayer.module.scss";

import React, { useRef, useState } from "react";

const VideoPlayer: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);

  const togglePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
    }
  };

  return (
    <div className={styles.videoPlayer}>
      <video
        ref={videoRef}
        width="1080"
        height="607"
        onTimeUpdate={handleTimeUpdate}
        controls
      >
        <source
          src="https://www.w3schools.com/html/mov_bbb.mp4"
          type="video/mp4"
        />
        Ваш браузер не поддерживает видео.
      </video>
      <p>Название видео</p>
    </div>
  );
};

export default VideoPlayer;
