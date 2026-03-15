import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import CircularProgress from "@mui/material/CircularProgress";
import RecipeGrid from "../components/RecipeGrid";
import CreateRecipeDialog from "../components/CreateRecipeDialog";
import defaultImage from "../assets/default-recipe.svg";
import HeroCarousel from "../components/HeroCarousel";
import Header from "../components/Header";

export default function Home() {
  const navigate = useNavigate();

  const [open, setOpen] = useState(false);
  const [recipes, setRecipes] = useState([]);
  const [recommendedRecipes, setRecommendedRecipes] = useState([]);
  const [loadingSaved, setLoadingSaved] = useState(false);

  useEffect(() => {
    let cancelled = false;

    const fetchSavedRecipes = async () => {
      if (!cancelled) {
        setLoadingSaved(true);
      }

      try {
        const res = await fetch("/api/recipe_list");

        if (!res.ok) throw new Error(`Request failed (${res.status})`);

        const data = await res.json();
        const list = Array.isArray(data) ? data : data?.items ?? [];

        if (!cancelled) {
          setRecipes(list.slice(0, 6));
          setRecommendedRecipes(list.slice(0, 3));
        }
      } catch (err) {
        if (!cancelled) {
          setRecipes([]);
          setRecommendedRecipes([]);
        }
      } finally {
        if (!cancelled) setLoadingSaved(false);
      }
    };

    fetchSavedRecipes();

    return () => {
      cancelled = true;
    };
  }, []);

  const handleCreate = (newRecipe) => {
    const recipeWithImage = {
      ...newRecipe,
      image: defaultImage,
      id: newRecipe.id ?? crypto.randomUUID?.() ?? String(Date.now()),
    };

    setRecipes((prev) => [recipeWithImage, ...prev].slice(0, 6));
  };

  return (
    <Box sx={{ bgcolor: "#f6f7f9", minHeight: "100vh" }}>
      <Header />
      <Container sx={{ py: 4 }}>
        <Box sx={{ display: "flex", flexDirection: "column", alignItems: "flex-start" }}>

          <HeroCarousel />
          <Box sx={{ display: "flex", gap: 2 }}>
            <Button
              variant="contained"
              onClick={() => setOpen(true)}
              sx={{
                backgroundColor: "#F6784C",
                "&:hover": { backgroundColor: "#e5673d" },
              }}
            >
              Create Recipe
            </Button>

            <Button
              variant="contained"
              onClick={() => navigate("/recipes")}
              sx={{
                backgroundColor: "#B7D400",
                "&:hover": { backgroundColor: "#a6c200" },
              }}
            >
              View All Recipes
            </Button>

            <Button
              variant="contained"
              onClick={() => navigate("/mealplans")}
              sx={{
                backgroundColor: "#E8A600",
                "&:hover": { backgroundColor: "#d39500" },
              }}
>
  Custom Meal Plan
</Button>


          </Box>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" fontWeight={800} sx={{ mb: 2 }}>
            Your Recipes
          </Typography>

          {loadingSaved ? (
            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
              <CircularProgress size={22} />
              <Typography>Loading recipes…</Typography>
            </Box>
          ) : recipes.length > 0 ? (
            <RecipeGrid recipes={recipes} />
          ) : (
            <Typography sx={{ opacity: 0.8 }}>
              No recipes saved.
            </Typography>
          )}
        </Box>

        <Divider sx={{ my: 4 }} />

        <Box>
          <Typography variant="h5" fontWeight={800} sx={{ mb: 2 }}>
            Recommended Recipes
          </Typography>

          {recommendedRecipes.length > 0 ? (
            <RecipeGrid recipes={recommendedRecipes} />
          ) : (
            <Typography sx={{ opacity: 0.8 }}>
              No recommended recipes available.
            </Typography>
          )}
        </Box>

        <CreateRecipeDialog
          open={open}
          onClose={() => setOpen(false)}
          onCreate={handleCreate}
        />
      </Container>
    </Box>
  );
}