import { useEffect, useMemo, useState } from "react";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import Chip from "@mui/material/Chip";
import IconButton from "@mui/material/IconButton";
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import Header from "../components/Header";
import RecipeSelectDialog from "../components/RecipeSelectDialog";

const MEAL_SLOTS = ["Breakfast", "Lunch", "Dinner"];

function formatDateKey(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatDisplayDate(date) {
  return date.toLocaleDateString("en-US", {
    weekday: "long",
    month: "short",
    day: "numeric",
  });
}

function getStartOfWeek(date) {
  const copy = new Date(date);
  const day = copy.getDay(); 
  copy.setDate(copy.getDate() - day);
  copy.setHours(0, 0, 0, 0);
  return copy;
}

function getWeekDates(selectedDate) {
  const start = getStartOfWeek(selectedDate);

  return Array.from({ length: 7 }, (_, index) => {
    const date = new Date(start);
    date.setDate(start.getDate() + index);
    return date;
  });
}

function formatWeekRange(start, end) {
  return `${start.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  })} – ${end.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  })}`;
}


function SlotCard({ slot, recipe, onAdd, onRemove }) {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 2,
        borderRadius: "16px",
        border: "1px solid #E6E8EC",
        backgroundColor: "#fff",
        minHeight: 170,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      <Box>
        <Typography
          variant="subtitle1"
          sx={{ fontWeight: 700, color: "#1F2937", mb: 1 }}
        >
          {slot}
        </Typography>

        {recipe ? (
          <>
            <Typography sx={{ color: "#374151", fontWeight: 700 }}>
              {recipe.title}
            </Typography>
            {recipe.cook_time != null && (
              <Typography sx={{ color: "#6B7280", mt: 0.5 }}>
                Cook time: {recipe.cook_time} min
              </Typography>
            )}
          </>
        ) : (
          <Typography sx={{ color: "#6B7280" }}>
            No recipe assigned.
          </Typography>
        )}
      </Box>

      <Box sx={{ mt: 2 }}>
        {recipe ? (
          <Button
            variant="outlined"
            color="error"
            size="small"
            onClick={onRemove}
          >
            Remove
          </Button>
        ) : (
          <Button
            variant="contained"
            size="small"
            onClick={onAdd}
            sx={{
              backgroundColor: "#B7D400",
              color: "#fff",
              "&:hover": { backgroundColor: "#a6c200" },
            }}
          >
            Add Recipe
          </Button>
        )}
      </Box>
    </Paper>
  );
}

function DayPlanCard({ date, plan, onAddRecipe, onRemoveRecipe }) {
  const dateKey = formatDateKey(date);

  return (
    <Paper
      elevation={0}
      sx={{
        p: 3,
        borderRadius: "24px",
        border: "1px solid #E6E8EC",
        backgroundColor: "#fff",
        height: "100%",
      }}
    >
      <Typography
        variant="h6"
        sx={{ fontWeight: 800, color: "#1F2937", mb: 2 }}
      >
        {formatDisplayDate(date)}
      </Typography>

      <Grid container spacing={2}>
        {MEAL_SLOTS.map((slot) => {
          const slotKey = slot.toLowerCase();
          const recipe = plan?.[slotKey] ?? null;

          return (
            <Grid key={slot}>
              <SlotCard
                slot={slot}
                recipe={recipe}
                onAdd={() => onAddRecipe(dateKey, slotKey)}
                onRemove={() => onRemoveRecipe(dateKey, slotKey)}
              />
            </Grid>
          );
        })}
      </Grid>
    </Paper>
  );
}

export default function MealPlansPage() {
  const [viewMode, setViewMode] = useState("week");
  const [selectedDate, setSelectedDate] = useState(new Date());

  const [mealPlan, setMealPlan] = useState({});
  const [availableRecipes, setAvailableRecipes] = useState([]);
  const [recipesLoading, setRecipesLoading] = useState(true);

  const [recipeDialogOpen, setRecipeDialogOpen] = useState(false);
  const [activeSlot, setActiveSlot] = useState(null);
  const [dirty, setDirty] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState("");

  const weekDates = useMemo(() => getWeekDates(selectedDate), [selectedDate]);

  const weekRangeLabel = useMemo(() => {
    if (!weekDates.length) return "";
    return formatWeekRange(weekDates[0], weekDates[6]);
  }, [weekDates]);

  useEffect(() => {
    let cancelled = false;

    const fetchRecipes = async () => {
      if (!cancelled) {
        setRecipesLoading(true);
      }

      try {
        const res = await fetch("/api/recipe_list");
        if (!res.ok) throw new Error(`Request failed (${res.status})`);

        const data = await res.json();
        const list = Array.isArray(data) ? data : [];

        if (!cancelled) {
          setAvailableRecipes(list);
        }
      } catch (err) {
        if (!cancelled) {
          setAvailableRecipes([]);
        }
      } finally {
        if (!cancelled) {
          setRecipesLoading(false);
        }
      }
    };

    fetchRecipes();

    return () => {
      cancelled = true;
    };
  }, []);

  const handleViewChange = (_, nextView) => {
    if (nextView) {
      setViewMode(nextView);
    }
  };

  const goToPreviousWeek = () => {
    setSelectedDate((prev) => {
      const next = new Date(prev);
      next.setDate(next.getDate() - 7);
      return next;
    });
  };

  const goToNextWeek = () => {
    setSelectedDate((prev) => {
      const next = new Date(prev);
      next.setDate(next.getDate() + 7);
      return next;
    });
  };

  const handleAddRecipe = (dateKey, slotKey) => {
    setActiveSlot({ dateKey, slotKey });
    setRecipeDialogOpen(true);
  };

  const handleSelectRecipe = (recipe) => {
    if (!activeSlot) return;

    const { dateKey, slotKey } = activeSlot;

    setMealPlan((prev) => ({
      ...prev,
      [dateKey]: {
        breakfast: prev[dateKey]?.breakfast ?? null,
        lunch: prev[dateKey]?.lunch ?? null,
        dinner: prev[dateKey]?.dinner ?? null,
        [slotKey]: {
          id: recipe.id,
          title: recipe.title,
          cook_time: recipe.cook_time ?? null,
        },
      },
    }));

    setDirty(true);
    setSaveMessage("");
    setRecipeDialogOpen(false);
    setActiveSlot(null);
  };

  const handleRemoveRecipe = (dateKey, slotKey) => {
    setMealPlan((prev) => ({
      ...prev,
      [dateKey]: {
        breakfast: prev[dateKey]?.breakfast ?? null,
        lunch: prev[dateKey]?.lunch ?? null,
        dinner: prev[dateKey]?.dinner ?? null,
        [slotKey]: null,
      },
    }));

    setDirty(true);
    setSaveMessage("");
  };

  const handleCloseDialog = () => {
    setRecipeDialogOpen(false);
    setActiveSlot(null);
  };

  const buildMealPlanPayload = () => {
    const plans = Object.fromEntries(
      Object.entries(mealPlan).map(([dateKey, slots]) => [
        dateKey,
        {
          breakfast: slots.breakfast?.id ?? null,
          lunch: slots.lunch?.id ?? null,
          dinner: slots.dinner?.id ?? null,
        },
      ])
    );

    return { plans };
  };

  const saveMealPlan = async () => {
    setSaving(true);
    setSaveMessage("");

    try {
      const payload = buildMealPlanPayload();

      const res = await fetch("/api/mealplan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`Request failed (${res.status})`);
      }

      setDirty(false);
      setSaveMessage("Meal plan saved.");
    } catch (err) {
      setSaveMessage("Could not save meal plan.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Box sx={{ bgcolor: "#f6f7f9", minHeight: "100vh" }}>
      <Header />

      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: { xs: "flex-start", md: "center" },
            flexDirection: { xs: "column", md: "row" },
            gap: 2,
            mb: 3,
          }}
        >
          <Box>
            <Typography
              variant="h4"
              sx={{ fontWeight: 800, color: "#1F2937" }}
            >
              Meal Planner
            </Typography>
            <Typography sx={{ color: "#6B7280", mt: 0.5 }}>
              Plan your meals by day or for the full week.
            </Typography>
          </Box>

          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1.5,
              flexWrap: "wrap",
            }}
          >
            {dirty && (
              <Chip
                label="Unsaved changes"
                sx={{
                  backgroundColor: "#FEF3C7",
                  color: "#92400E",
                  fontWeight: 700,
                }}
              />
            )}

            <Button
              variant="contained"
              onClick={saveMealPlan}
              disabled={saving}
              sx={{
                backgroundColor: "#F6784C",
                fontWeight: 700,
                "&:hover": { backgroundColor: "#e5673d" },
              }}
            >
              {saving ? "Saving..." : "Save Plan"}
            </Button>
          </Box>
        </Box>

        {saveMessage && (
          <Typography
            sx={{
              mb: 2,
              color: saveMessage.includes("saved") ? "#166534" : "#B91C1C",
              fontWeight: 600,
            }}
          >
            {saveMessage}
          </Typography>
        )}

        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: { xs: "flex-start", md: "center" },
            flexDirection: { xs: "column", md: "row" },
            gap: 2,
            mb: 3,
          }}
        >
          <ToggleButtonGroup
            value={viewMode}
            exclusive
            onChange={handleViewChange}
            size="small"
            sx={{
              backgroundColor: "#fff",
              borderRadius: "14px",
              "& .MuiToggleButton-root": {
                px: 2,
                py: 1,
                border: "1px solid #E6E8EC",
                textTransform: "none",
                fontWeight: 700,
              },
              "& .Mui-selected": {
                backgroundColor: "#F6784C !important",
                color: "#fff",
              },
            }}
          >
            <ToggleButton value="day">Day View</ToggleButton>
            <ToggleButton value="week">Week View</ToggleButton>
          </ToggleButtonGroup>

          {viewMode === "week" && (
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 1,
                px: 1,
                py: 0.5,
                borderRadius: "999px",
                backgroundColor: "#fff",
                border: "1px solid #E6E8EC",
              }}
            >
              <IconButton
                onClick={goToPreviousWeek}
                size="small"
                sx={{ color: "#F6784C" }}
              >
                <ArrowBackIosNewIcon fontSize="inherit" />
              </IconButton>

              <Typography
                sx={{
                  minWidth: 170,
                  textAlign: "center",
                  fontWeight: 700,
                  color: "#1F2937",
                }}
              >
                {weekRangeLabel}
              </Typography>

              <IconButton
                onClick={goToNextWeek}
                size="small"
                sx={{ color: "#F6784C" }}
              >
                <ArrowForwardIosIcon fontSize="inherit" />
              </IconButton>
            </Box>
          )}
        </Box>

        <Divider sx={{ mb: 3 }} />

        {viewMode === "day" ? (
          <DayPlanCard
            date={selectedDate}
            plan={mealPlan[formatDateKey(selectedDate)]}
            onAddRecipe={handleAddRecipe}
            onRemoveRecipe={handleRemoveRecipe}
          />
        ) : (
          <Grid container spacing={3}>
            {weekDates.map((date) => {
              const dateKey = formatDateKey(date);
              const plan = mealPlan[dateKey];

              return (
                <Grid key={dateKey}>
                  <DayPlanCard
                    date={date}
                    plan={plan}
                    onAddRecipe={handleAddRecipe}
                    onRemoveRecipe={handleRemoveRecipe}
                  />
                </Grid>
              );
            })}
          </Grid>
        )}

        <RecipeSelectDialog
          open={recipeDialogOpen}
          recipes={availableRecipes}
          loading={recipesLoading}
          onClose={handleCloseDialog}
          onSelect={handleSelectRecipe}
        />
      </Container>
    </Box>
  );
}
