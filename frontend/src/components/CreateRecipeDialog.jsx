import { useEffect, useMemo, useState } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Stack from "@mui/material/Stack";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import Divider from "@mui/material/Divider";
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";

const emptyIngredient = () => ({ name: "", quantity: "", unit: "" });

export default function CreateRecipeDialog({ open, onClose, onCreate }) {
  const [title, setTitle] = useState("");
  const [instructions, setInstructions] = useState("");
  const [cookingTimeMinutes, setCookingTimeMinutes] = useState("");
  const [ingredients, setIngredients] = useState([emptyIngredient()]);

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const canSubmit = useMemo(() => {
    const trimmedTitle = title.trim();
    const trimmedInstructions = instructions.trim();
    const timeNum = Number(cookingTimeMinutes);

    const cleanIngredients = ingredients
      .map((i) => ({
        name: i.name.trim(),
        quantity: Number(i.quantity),
        unit: i.unit.trim(),
      }))
      .filter((i) => i.name && i.unit && Number.isFinite(i.quantity) && i.quantity > 0);

    return (
      trimmedTitle.length > 0 &&
      trimmedInstructions.length > 0 &&
      cleanIngredients.length > 0 &&
      Number.isFinite(timeNum) &&
      timeNum > 0
    );
  }, [title, instructions, ingredients, cookingTimeMinutes]);

  useEffect(() => {
    if (!open) {
      setTitle("");
      setInstructions("");
      setCookingTimeMinutes("");
      setIngredients([emptyIngredient()]);
      setSubmitting(false);
      setError("");
    }
  }, [open]);

  const updateIngredient = (idx, key, value) => {
    setIngredients((prev) =>
      prev.map((ing, i) => (i === idx ? { ...ing, [key]: value } : ing))
    );
  };

  const addIngredient = () => setIngredients((prev) => [...prev, emptyIngredient()]);

  const removeIngredient = (idx) =>
    setIngredients((prev) => prev.filter((_, i) => i !== idx));

  const handleSubmit = async () => {
    setError("");

    const payload = {
      title: title.trim(),
      instructions: instructions.trim(),
      cookingTimeMinutes: Number(cookingTimeMinutes),
      ingredients: ingredients
        .map((i) => ({
          name: i.name.trim(),
          quantity: Number(i.quantity),
          unit: i.unit.trim(),
        }))
        .filter((i) => i.name && i.unit && Number.isFinite(i.quantity) && i.quantity > 0),
    };

    onCreate?.(payload);

    setSubmitting(true);
    try {
      const res = await fetch("/api/recipe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        let msg = `Request failed (${res.status})`;
        try {
          const data = await res.json();
          msg = data?.detail || data?.message || msg;
        } catch {
          // ignore
        }
        throw new Error(msg);
      }

      onClose?.();
    } catch (e) {
      setError(e?.message || "Failed to save recipe.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onClose={submitting ? undefined : onClose} fullWidth maxWidth="sm">
      <DialogTitle>Create Recipe</DialogTitle>

      <DialogContent>
        <Stack spacing={2} sx={{ mt: 1 }}>
          {error ? <Alert severity="error">{error}</Alert> : null}

          <TextField
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            fullWidth
            autoFocus
          />

          <TextField
            label="Cooking time (minutes)"
            value={cookingTimeMinutes}
            onChange={(e) => {
              const v = e.target.value;
              if (v === "" || /^[0-9]+$/.test(v)) setCookingTimeMinutes(v);
            }}
            inputMode="numeric"
            fullWidth
          />

          <Divider />

          <Stack direction="row" alignItems="center" justifyContent="space-between">
            <Typography fontWeight={700}>Ingredients</Typography>
            <Button onClick={addIngredient} startIcon={<AddIcon />}>
              Add
            </Button>
          </Stack>

          <Stack spacing={1}>
            {ingredients.map((ing, idx) => (
              <Stack key={idx} direction={{ xs: "column", sm: "row" }} spacing={1} alignItems="center">
                <TextField
                  label="Name"
                  value={ing.name}
                  onChange={(e) => updateIngredient(idx, "name", e.target.value)}
                  fullWidth
                />

                <TextField
                  label="Qty"
                  value={ing.quantity}
                  onChange={(e) => {
                    const v = e.target.value;
                    if (v === "" || /^[0-9]*\.?[0-9]*$/.test(v)) {
                      updateIngredient(idx, "quantity", v);
                    }
                  }}
                  inputMode="decimal"
                  sx={{ width: { xs: "100%", sm: 120 } }}
                />

                <TextField
                  label="Unit"
                  value={ing.unit}
                  onChange={(e) => updateIngredient(idx, "unit", e.target.value)}
                  sx={{ width: { xs: "100%", sm: 140 } }}
                />

                <IconButton
                  aria-label="Remove ingredient"
                  onClick={() => removeIngredient(idx)}
                  disabled={ingredients.length === 1}
                >
                  <DeleteIcon />
                </IconButton>
              </Stack>
            ))}
          </Stack>

          <Divider />

          <TextField
            label="Instructions"
            value={instructions}
            onChange={(e) => setInstructions(e.target.value)}
            fullWidth
            multiline
            minRows={4}
          />
        </Stack>
      </DialogContent>

      <DialogActions sx={{ px: 3, pb: 2 }}>
        <Button onClick={onClose} disabled={submitting}>
          Cancel
        </Button>
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={!canSubmit || submitting}
          sx={{
            backgroundColor: "#F6784C",
            "&:hover": { backgroundColor: "#e5673d" },
          }}
        >
          {submitting ? "Saving..." : "Save"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}