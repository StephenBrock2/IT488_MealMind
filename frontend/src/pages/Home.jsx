import { useState, useEffect } from "react";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import RecipeGrid from "../components/RecipeGrid";
import CreateRecipeDialog from "../components/CreateRecipeDialog";
import logo from "../assets/mealmind-logo.png";
import defaultImage from "../assets/default-recipe.svg";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";

export default function Home() {
  const [open, setOpen] = useState(false);

  const [recipes, setRecipes] = useState([]);
  const [loadingSaved, setLoadingSaved] = useState(false);
  const [savedError, setSavedError] = useState("");

  useEffect(() => {
  let cancelled = false;

  const fetchSavedRecipes = async () => {
    if (!cancelled) {
      setSavedError("");
      setLoadingSaved(true);
    }

    try {
      const res = await fetch("/api/recipe?limit=6");

      if (res.status === 404) {
        if (!cancelled) setRecipes([]);
        return;
      }

      if (!res.ok) throw new Error(`Request failed (${res.status})`);

      const data = await res.json();
      const list = Array.isArray(data) ? data : data?.items ?? [];

      if (!cancelled) setRecipes(list.slice(0, 6));
    } catch (err) {
      if (!cancelled) {
        setSavedError("Oops — couldn’t load recipes right now.");
        setRecipes([]);
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
      <Container sx={{ py: 4 }}>
        <Box sx={{ display: "flex", flexDirection: "column", alignItems: "flex-start" }}>
          <Box
            component="img"
            src={logo}
            alt="MealMind Logo"
            sx={{ width: 220, height: "auto", mb: 2, mt: -8}}
          />

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
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" fontWeight={800} sx={{ mb: 2 }}>
            Your Recipes
          </Typography>

          {savedError ? <Alert severity="error" sx={{ mb: 2 }}>{savedError}</Alert> : null}

          {loadingSaved ? (
            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
              <CircularProgress size={22} />
              <Typography>Loading saved recipes…</Typography>
            </Box>
          ) : recipes.length > 0 ? (
            <RecipeGrid recipes={recipes} />
          ) : (
            <Typography sx={{ opacity: 0.8 }}>
              No saved recipes yet. Click <b>Create Recipe</b> to add one.
            </Typography>
          )}
        </Box>

        <Divider sx={{ my: 4 }} />

        <Box>
          <Typography variant="h5" fontWeight={800} sx={{ mb: 2 }}>
            Recommended Recipes
          </Typography>
          <RecipeGrid />
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