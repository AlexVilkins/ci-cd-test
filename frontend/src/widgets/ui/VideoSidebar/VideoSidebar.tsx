import React from "react";

import styles from "./VideoSidebar.module.scss";

interface Video {
  id: number;
  title: string;
  thumbnail: string;
}

const recommendedVideos: Video[] = [
  {
    id: 1,
    title: "Как создать приложение на React",
    thumbnail: "https://via.placeholder.com/150",
  },
  {
    id: 2,
    title: "Понимание TypeScript",
    thumbnail: "https://via.placeholder.com/150",
  },
  {
    id: 3,
    title: "Введение в Redux",
    thumbnail: "https://via.placeholder.com/150",
  },
  {
    id: 4,
    title: "CSS Flexbox для начинающих",
    thumbnail: "https://via.placeholder.com/150",
  },
  {
    id: 5,
    title: "CSS Flexbox для начинающих",
    thumbnail: "https://via.placeholder.com/150",
  },
  {
    id: 6,
    title: "CSS Flexbox для начинающих",
    thumbnail: "https://via.placeholder.com/150",
  },
  {
    id: 7,
    title: "CSS Flexbox для начинающих",
    thumbnail: "https://via.placeholder.com/150",
  },
];

const VideoSidebar: React.FC = () => {
  return (
    <div className={styles.videoSidebar}>
      <h3>История</h3>
      <ul className={styles.videoList}>
        {recommendedVideos.map((video) => (
          <li key={video.id} className={styles.video}>
            <video
              className={styles.videoThumbnail}
              //   ref={video.thumbnail}
              controls
              width="300"
              height="160"
              //   src={video.thumbnail}
              //   alt={video.title}
              //   style={{ width: "80px", height: "auto", marginRight: "10px" }}
            >
              <source src={video.thumbnail} type="video/mp4" />
            </video>
            <p className={styles.videoTitle}>{video.title}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VideoSidebar;
