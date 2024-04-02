import "./App.scss";
import Routers from "router";
import { BrowserRouter as Router } from "react-router-dom";
import { Header, Footer } from "components";

function App() {
  return (
    <Router>
      <Header />
      <Routers />
      <Footer />
    </Router>
  );
}

export default App;
