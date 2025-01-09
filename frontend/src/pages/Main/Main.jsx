import styles from "./Main.module.scss";

import { getData } from "../../app/api/getData";
import { useEffect, useState } from "react";

export default function Main() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await getData();
      setData(response);
    };
    fetchData();
  }, []);
  // const data = getData();

  return (
    <div className={styles.main}>
      <p>People: </p>
      {data.map((item) => (
        <div key={item.id}>
          <p>
            {item.name} {item.age} {item.city}
          </p>
        </div>
      ))}
    </div>
  );
}
