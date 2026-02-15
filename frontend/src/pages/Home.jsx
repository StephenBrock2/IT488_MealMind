import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import RecipeGrid from "../components/RecipeGrid";
import { useEffect } from "react";
import logo from "../assets/mealmind-logo.png";


export default function Home() {
  useEffect(() => {
    fetch("/api/health")
      .then((res) => res.json())
      .then((data) => console.log("Backend connected:", data))
      .catch((err) => console.error("API error:", err));
  }, []);

  return (
    <Box sx={{ bgcolor: "#f6f7f9", minHeight: "100vh" }}>
      <Container sx={{ py: 5 }}>
        <Box
          component="img"
          src={logo}
          alt="MealMind Logo"
          sx={{ mb: 4, mt: 0, width: 220, height: "auto" }}
        />

        <Typography variant="h5" fontWeight={800} sx={{ mb: 3 }}>
          Recommended Recipes
        </Typography>

        <RecipeGrid />
      </Container>
    </Box>
  );
}
