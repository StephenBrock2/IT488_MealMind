import { useEffect, useState } from "react";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";
import SavedRecipesTable from "../components/SavedRecipesTable";
import Header from "../components/Header";


export default function RecipesPage() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const res = await fetch("/api/recipe_list");
        const data = await res.json();
        setRecipes(Array.isArray(data) ? data : []);
      } catch (err) {
        setRecipes([]);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, []);

  return (
    <Box sx={{ bgcolor: "#f6f7f9", minHeight: "100vh" }}>
    <Header />
    <Container maxWidth="xl" sx={{ py: 0 }}>


      {loading ? (
        <CircularProgress />
      ) : (
        <SavedRecipesTable recipes={recipes} />
      )}
    </Container>
    </Box>
  );
}