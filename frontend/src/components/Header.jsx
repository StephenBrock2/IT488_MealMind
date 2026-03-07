import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import { useNavigate } from "react-router-dom";
import logo from "../assets/mealmind-logo.png";

export default function Header() {
  const navigate = useNavigate();

  return (
    <Box >
      <Container maxWidth="lg" sx={{ pt: 0, pb: 0, margin: 0 }}>
        <Box
          component="img"
          src={logo}
          alt="MealMind Logo"
          onClick={() => navigate("/")}
          sx={{
            width: 220,
            height: "auto",
            cursor: "pointer",
            display: "block",
          }}
        />
      </Container>
    </Box>
  );
}