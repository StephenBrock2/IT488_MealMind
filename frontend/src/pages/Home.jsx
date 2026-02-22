import { useState } from "react";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";

import RecipeGrid from "../components/RecipeGrid";
import CreateRecipeDialog from "../components/CreateRecipeDialog";
import logo from "../assets/mealmind-logo.png";
import defaultImage from "../assets/default-recipe.svg";

export default function Home() {
  const [open, setOpen] = useState(false);
  const [recipes, setRecipes] = useState([]);

  const handleCreate = (newRecipe) => {
    const recipeWithImage = {
      ...newRecipe,
      image: defaultImage,
      id: newRecipe.id ?? crypto.randomUUID?.() ?? String(Date.now()),
    };

    setRecipes((prev) => [recipeWithImage, ...prev]);
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

        {recipes.length > 0 && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" fontWeight={800} sx={{ mb: 2 }}>
              Your Recipes
            </Typography>
            <RecipeGrid recipes={recipes} />
          </Box>
        )}

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