import { Provider } from "react-redux";
import { store } from "@app/redux/store";

import Main from "./pages/Main/Main";

import "./App.css";

function App() {
  return (
    <Provider store={store}>
      <Main />
    </Provider>
  );
}

export default App;
