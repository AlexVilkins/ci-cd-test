import styles from "./Main.module.scss";

import MainPanel from "@widgets/ui/MainPanel/MainPanel";
import VideoPlayer from "@widgets/ui/VideoPlayer/VideoPlayer";
import VideoSidebar from "@widgets/ui/VideoSidebar/VideoSidebar";

export default function Main() {
  return (
    <div className={styles.main}>
      <div className={styles.container}>
        <MainPanel />
        <VideoPlayer />
      </div>

      <VideoSidebar />
    </div>
  );
}
