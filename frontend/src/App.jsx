import Home from "./pages/Home";
import RecipesPage from "./pages/RecipesPage";
import MealPlansPage from "./pages/MealPlansPage";
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={<Home />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/recipes" element={<RecipesPage />} />
      <Route path="/mealplans" element={<MealPlansPage />} />
      <Route path="*" element={<Navigate to="/login" />} />

    </Routes>
  );
}

export default App;