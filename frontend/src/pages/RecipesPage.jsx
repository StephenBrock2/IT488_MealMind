import { useEffect, useState } from "react";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
import Header from "../components/Header";
import SavedRecipesTable from "../components/SavedRecipesTable";

export default function RecipesPage() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pageMessage, setPageMessage] = useState("");
  const [deletingRecipeId, setDeletingRecipeId] = useState(null);

  useEffect(() => {
    let cancelled = false;

    const fetchRecipes = async () => {
      if (!cancelled) {
        setLoading(true);
        setPageMessage("");
      }

      try {
        const res = await fetch("/api/recipe_list", {
          credentials: "include",
        });

        if (!res.ok) {
          throw new Error(`Request failed (${res.status})`);
        }

        const data = await res.json();
        const recipeList = Array.isArray(data) ? data : [];

        if (!cancelled) {
          setRecipes(recipeList);
        }
      } catch (err) {
        if (!cancelled) {
          setRecipes([]);
          setPageMessage("Could not load recipes.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchRecipes();

    return () => {
      cancelled = true;
    };
  }, []);

  const handleDeleteRecipe = async (recipe) => {
    if (!recipe?.id) return;

    setDeletingRecipeId(recipe.id);
    setPageMessage("");

    try {
      const res = await fetch(`/api/recipe/${recipe.id}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (res.status === 401) {
        throw new Error("Not authenticated");
      }

      if (res.status === 403) {
        throw new Error("Forbidden");
      }

      if (!res.ok) {
        throw new Error(`Delete failed (${res.status})`);
      }

      setRecipes((prev) => prev.filter((r) => r.id !== recipe.id));
      setPageMessage("Recipe deleted.");
    } catch (err) {
      if (err.message === "Not authenticated") {
        setPageMessage("You must be logged in to delete a recipe.");
      } else if (err.message === "Forbidden") {
        setPageMessage("You can only delete your own recipes.");
      } else {
        setPageMessage("Could not delete recipe.");
      }
    } finally {
      setDeletingRecipeId(null);
    }
  };

  return (
    <Box sx={{ bgcolor: "#f6f7f9", minHeight: "100vh" }}>
      <Header />

      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ mb: 3 }}>
          <Typography
            variant="h4"
            sx={{ fontWeight: 800, color: "#1F2937" }}
          >
            Saved Recipes
          </Typography>
          <Typography sx={{ color: "#6B7280", mt: 0.5 }}>
            View, expand, filter, and delete your saved recipes.
          </Typography>
        </Box>

        {pageMessage && (
          <Alert
            severity={pageMessage.toLowerCase().includes("deleted") ? "success" : "error"}
            sx={{ mb: 3 }}
          >
            {pageMessage}
          </Alert>
        )}

        {loading ? (
          <Box
            sx={{
              minHeight: 220,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <CircularProgress />
          </Box>
        ) : (
          <SavedRecipesTable
            recipes={recipes}
            onDeleteRecipe={handleDeleteRecipe}
            deletingRecipeId={deletingRecipeId}
          />
        )}
      </Container>
    </Box>
  );
}