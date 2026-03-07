import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import RecipesPage from "./pages/RecipesPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/recipes" element={<RecipesPage />} />
    </Routes>
  );
}

export default App;