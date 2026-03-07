import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";
import StarIcon from "@mui/icons-material/Star";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import BookmarkBorderIcon from "@mui/icons-material/BookmarkBorder";

import defaultRecipeImage from "../assets/default-recipe.svg";

function normalizeRecipe(r) {
  const id = r.id ?? crypto.randomUUID?.() ?? String(Date.now() + Math.random());

  const img = r.img || r.image || defaultRecipeImage;

  const minutes =
    r.cookingTimeMinutes ??
    r.cooking_time_minutes ??
    r.cook_time ??
    (typeof r.time === "string" ? null : r.time);

  const time =
    typeof r.time === "string"
      ? r.time
      : Number.isFinite(Number(minutes)) && Number(minutes) > 0
        ? `${Number(minutes)} min`
        : "—";

  const rating = typeof r.rating === "number" ? r.rating : 0;

  return { ...r, id, img, time, rating };
}

function RecipeCard({ recipe }) {
  const r = normalizeRecipe(recipe);

  return (
    <Card sx={{ borderRadius: 3, overflow: "hidden" }} data-testid="recipe-card">
      <CardMedia component="img" height="160" image={r.img} alt={r.title} />
      <CardContent sx={{ pb: 1 }}>
        <Typography variant="subtitle1" fontWeight={700}>
          {r.title}
        </Typography>

        <Stack direction="row" alignItems="center" spacing={0.5}>
          <StarIcon fontSize="small" />
          <Typography variant="body2">{r.rating ? r.rating.toFixed(1) : "—"}</Typography>
          <Typography variant="body2" sx={{ ml: "auto", fontWeight: 700 }}>
            {r.time}
          </Typography>
        </Stack>
      </CardContent>

      <CardActions disableSpacing sx={{ pt: 0 }}>
        <IconButton aria-label="favorite">
          <FavoriteBorderIcon />
        </IconButton>
        <IconButton aria-label="save">
          <BookmarkBorderIcon />
        </IconButton>
      </CardActions>
    </Card>
  );
}

export default function RecipeGrid({ recipes = [] }) {
  const list = recipes.map(normalizeRecipe);

  return (
    <Grid container spacing={2}>
      {list.map((r) => (
        <Grid key={r.id}>
          <RecipeCard recipe={r} />
        </Grid>
      ))}
    </Grid>
  );
}