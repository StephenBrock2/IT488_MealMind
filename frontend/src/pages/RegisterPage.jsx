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
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

export default function RegisterPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const updateField = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
    setErrors((prev) => ({ ...prev, [key]: "" }));
    setSubmitError("");
  };

  const validate = () => {
    const e = {};

    if (!form.firstName.trim()) {
      e.firstName = "First name is required.";
    }

    if (!form.lastName.trim()) {
      e.lastName = "Last name is required.";
    }

    if (!form.email.trim()) {
      e.email = "Email is required.";
    } else if (!emailRegex.test(form.email.trim())) {
      e.email = "Enter a valid email address.";
    }

    if (!form.password) {
      e.password = "Password is required.";
    } else if (!passwordRegex.test(form.password)) {
      e.password =
        "Password must be at least 8 characters and include uppercase, lowercase, and a number.";
    }

    return e;
  };

  const isValid = useMemo(() => {
    return (
      form.firstName.trim() &&
      form.lastName.trim() &&
      emailRegex.test(form.email.trim()) &&
      passwordRegex.test(form.password)
    );
  }, [form]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError("");

    const validationErrors = validate();
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length > 0) return;

    setSubmitting(true);

    try {
      const response = await fetch("/api/user/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: form.email.trim(),
          email: form.email.trim(),
          password: form.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create account.");
      }

      navigate("/login");
    } catch (err) {
      setSubmitError(err.message || "Failed to create account.");
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
              Create your account
            </Typography>
          </Box>

          <Box sx={{ p: 3 }}>
            {submitError && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {submitError}
              </Alert>
            )}

            <Box component="form" role="form" onSubmit={handleSubmit}>
              <Stack spacing={2}>
                <TextField
                  label="First Name"
                  value={form.firstName}
                  onChange={(e) => updateField("firstName", e.target.value)}
                  error={!!errors.firstName}
                  helperText={errors.firstName}
                  fullWidth
                />

                <TextField
                  label="Last Name"
                  value={form.lastName}
                  onChange={(e) => updateField("lastName", e.target.value)}
                  error={!!errors.lastName}
                  helperText={errors.lastName}
                  fullWidth
                />

                <TextField
                  label="Email"
                  type="email"
                  value={form.email}
                  onChange={(e) => updateField("email", e.target.value)}
                  error={!!errors.email}
                  helperText={
                    errors.email || 'Email must be in "name@domain.info" format'
                  }
                  fullWidth
                />

                <TextField
                  label="Password"
                  type="password"
                  value={form.password}
                  onChange={(e) => updateField("password", e.target.value)}
                  error={!!errors.password}
                  helperText={
                    errors.password ||
                    "At least 8 characters, with uppercase, lowercase, and a number."
                  }
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
                  {submitting ? "Creating Account..." : "Create Account"}
                </Button>

                <Typography variant="body2" sx={{ textAlign: "center" }}>
                  Already have an account?{" "}
                  <Box
                    component="span"
                    onClick={() => navigate("/login")}
                    sx={{
                      color: "#F6784C",
                      fontWeight: 600,
                      cursor: "pointer",
                      "&:hover": { textDecoration: "underline" },
                    }}
                  >
                    Sign in
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