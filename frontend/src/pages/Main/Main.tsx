import styles from "./Main.module.scss";

import { getData } from "../../app/api/getData";
import MainPanel from "@widgets/ui/MainPanel/MainPanel";
import { useEffect, useState } from "react";

interface Person {
  id: string;
  name: string;
  age: number;
  city: string | null;
}

export default function Main() {
  const [data, setData] = useState<Person[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await getData();
      setData(response);
    };
    fetchData();
  }, []);

  return (
    <div className={styles.main}>
      {/* <p>People: </p>
      {data.map((item) => (
        <div key={item.id}>
          <p>
            {item.name} {item.age} {item.city}
          </p>
        </div>
      ))} */}
      <MainPanel />
    </div>
  );
}
