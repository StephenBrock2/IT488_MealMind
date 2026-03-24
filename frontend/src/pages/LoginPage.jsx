import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import Alert from "@mui/material/Alert";

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const isValid = useMemo(() => {
    return emailRegex.test(email.trim()) && password.length > 0;
  }, [email, password]);

  const validate = () => {
    const e = {};

    if (!email.trim()) {
      e.email = "Email is required.";
    } else if (!emailRegex.test(email.trim())) {
      e.email = "Enter a valid email address.";
    }

    if (!password) {
      e.password = "Password is required.";
    }

    return e;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError("");

    const validationErrors = validate();
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length > 0) return;

    setSubmitting(true);

    try {
      await new Promise((r) => setTimeout(r, 500));

      navigate("/dashboard");
    } catch {
      setSubmitError("Invalid email or password.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box sx={{ bgcolor: "#f6f7f9", minHeight: "100vh" }}>
      <Container maxWidth="sm" sx={{ py: 8 }}>
        <Paper
          elevation={0}
          sx={{
            borderRadius: 4,
            overflow: "hidden",
            boxShadow: "0 8px 24px rgba(0,0,0,0.08)",
          }}
        >
          <Box
            sx={{
              backgroundColor: "#F6784C",
              color: "white",
              p: 3,
            }}
          >
            <Typography variant="h5" fontWeight={800}>
              MealMind
            </Typography>
            <Typography sx={{ opacity: 0.9 }}>
              Welcome back
            </Typography>
          </Box>
          
          <Box sx={{ p: 3 }}>
            {submitError && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {submitError}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit}>
              <Stack spacing={2}>
                <TextField
                  label="Email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  error={!!errors.email}
                  helperText={errors.email}
                  fullWidth
                />

                <TextField
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  error={!!errors.password}
                  helperText={errors.password}
                  fullWidth
                />

                <Button
                  type="submit"
                  variant="contained"
                  disabled={!isValid || submitting}
                  sx={{
                    backgroundColor: "#F6784C",
                    "&:hover": { backgroundColor: "#e5673d" },
                  }}
                >
                  {submitting ? "Signing in..." : "Login"}
                </Button>

                <Typography variant="body2" sx={{ textAlign: "center" }}>
  Don’t have an account?{" "}
  <Box
    component="span"
    onClick={() => navigate("/register")}
    sx={{
      color: "#F6784C",
      fontWeight: 600,
      cursor: "pointer",
      "&:hover": { textDecoration: "underline" },
    }}
  >
    Create one
  </Box>
                </Typography>
              </Stack>
            </Box>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}