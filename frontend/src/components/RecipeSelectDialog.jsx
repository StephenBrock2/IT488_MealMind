import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";

export default function RecipeSelectDialog({
  open,
  recipes,
  loading,
  onClose,
  onSelect,
}) {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
      PaperProps={{
        sx: {
          borderRadius: "20px",
          overflow: "hidden",
        },
      }}
    >
      <DialogTitle
        sx={{
          backgroundColor: "#F6784C",
          color: "#fff",
          fontWeight: 800,
          fontSize: "1.2rem",
        }}
      >
        Select a Recipe
      </DialogTitle>

      <DialogContent
        dividers
        sx={{
          backgroundColor: "#F9FAFB",
          p: 0,
        }}
      >
        {loading ? (
          <Box sx={{ display: "flex", alignItems: "center", gap: 2, p: 3 }}>
            <CircularProgress size={22} />
            <Typography>Loading recipes...</Typography>
          </Box>
        ) : recipes.length > 0 ? (
          <List sx={{ p: 0 }}>
            {recipes.map((recipe) => (
              <ListItemButton
                key={recipe.id}
                onClick={() => onSelect(recipe)}
                sx={{
                  py: 2,
                  px: 3,
                  borderBottom: "1px solid #E6E8EC",
                  transition: "all 0.15s ease",
                  "&:hover": {
                    backgroundColor: "#ECFDF5",
                  },
                }}
              >
                <ListItemText
                  primary={
                    <Typography sx={{ fontWeight: 700 }}>
                      {recipe.title}
                    </Typography>
                  }
                  secondary={
                    recipe.cook_time != null
                      ? `Cook time: ${recipe.cook_time} min`
                      : "No cook time listed"
                  }
                />
                <ArrowForwardIosIcon sx={{ fontSize: 16, color: "#9CA3AF" }} />
              </ListItemButton>
            ))}
          </List>
        ) : (
          <Typography sx={{ p: 3, color: "#6B7280" }}>
            No saved recipes available.
          </Typography>
        )}
      </DialogContent>

      <DialogActions
        sx={{
          px: 3,
          py: 2,
          backgroundColor: "#F9FAFB",
        }}
      >
        <Button
          onClick={onClose}
          variant="contained"
          sx={{
            backgroundColor: "#B7D400",
            "&:hover": { backgroundColor: "#a6c200" },
            fontWeight: 700,
          }}
        >
          Cancel
        </Button>
      </DialogActions>
    </Dialog>
  );
}
