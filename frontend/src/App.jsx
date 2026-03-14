import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import RecipesPage from "./pages/RecipesPage";
import MealPlansPage from "./pages/MealPlansPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/recipes" element={<RecipesPage />} />
      <Route path="/mealplans" element={<MealPlansPage />} />
    </Routes>
  );
}

export default App;