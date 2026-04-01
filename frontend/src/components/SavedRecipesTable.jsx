import * as React from "react";
import PropTypes from "prop-types";
import { alpha } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Collapse from "@mui/material/Collapse";
import Checkbox from "@mui/material/Checkbox";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import TableSortLabel from "@mui/material/TableSortLabel";
import TextField from "@mui/material/TextField";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import { visuallyHidden } from "@mui/utils";
import { colors } from "../constants/colors";

function descendingComparator(a, b, orderBy) {
  const aValue = a[orderBy] ?? "";
  const bValue = b[orderBy] ?? "";

  if (typeof aValue === "string" && typeof bValue === "string") {
    return bValue.localeCompare(aValue);
  }

  if (bValue < aValue) return -1;
  if (bValue > aValue) return 1;
  return 0;
}

function getComparator(order, orderBy) {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

const headCells = [
  {
    id: "title",
    numeric: false,
    disablePadding: true,
    label: "Recipe Title",
  },
];

function EnhancedTableHead(props) {
  const {
    onSelectAllClick,
    order,
    orderBy,
    numSelected,
    rowCount,
    onRequestSort,
  } = props;

  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow
        sx={{
          backgroundColor: colors.greenSoft,
          "& th": {
            borderBottom: `1px solid ${colors.border}`,
          },
        }}
      >
        <TableCell width={60} />
        <TableCell padding="checkbox">
          <Checkbox
            color="default"
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            sx={{
              color: colors.green,
              "&.Mui-checked": {
                color: colors.green,
              },
              "&.MuiCheckbox-indeterminate": {
                color: colors.green,
              },
            }}
          />
        </TableCell>

        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.numeric ? "right" : "left"}
            padding={headCell.disablePadding ? "none" : "normal"}
            sortDirection={orderBy === headCell.id ? order : false}
            sx={{
              color: colors.textPrimary,
              fontWeight: 700,
              fontSize: "0.95rem",
            }}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : "asc"}
              onClick={createSortHandler(headCell.id)}
              sx={{
                color: `${colors.textPrimary} !important`,
                "& .MuiTableSortLabel-icon": {
                  color: `${colors.orange} !important`,
                },
                "&.Mui-active": {
                  color: `${colors.green} !important`,
                },
              }}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === "desc" ? "sorted descending" : "sorted ascending"}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}

        <TableCell
          align="right"
          sx={{
            color: colors.textPrimary,
            fontWeight: 700,
            fontSize: "0.95rem",
            pr: 3,
            width: 140,
          }}
        >
          Actions
        </TableCell>
      </TableRow>
    </TableHead>
  );
}

EnhancedTableHead.propTypes = {
  numSelected: PropTypes.number.isRequired,
  onRequestSort: PropTypes.func.isRequired,
  onSelectAllClick: PropTypes.func.isRequired,
  order: PropTypes.oneOf(["asc", "desc"]).isRequired,
  orderBy: PropTypes.string.isRequired,
  rowCount: PropTypes.number.isRequired,
};

function EnhancedTableToolbar({ numSelected, filterText, onFilterChange }) {
  return (
    <Toolbar
      sx={[
        {
          px: { xs: 2, sm: 3 },
          py: 2,
          display: "flex",
          gap: 2,
          flexWrap: "wrap",
          borderBottom: `1px solid ${colors.border}`,
          background: `linear-gradient(180deg, ${colors.white} 0%, #FCFCFC 100%)`,
        },
        numSelected > 0 && {
          bgcolor: alpha(colors.green, 0.08),
        },
      ]}
    >
      {numSelected > 0 ? (
        <Typography
          sx={{ flex: "1 1 200px", fontWeight: 700, color: colors.green }}
          color="inherit"
          variant="subtitle1"
        >
          {numSelected} selected
        </Typography>
      ) : (
        <Box sx={{ flex: "1 1 200px" }}>
          <Typography
            variant="h6"
            id="tableTitle"
            sx={{
              fontWeight: 800,
              color: colors.textPrimary,
              lineHeight: 1.2,
            }}
          >
            Saved Recipes
          </Typography>
          <Typography
            variant="body2"
            sx={{ color: colors.textSecondary, mt: 0.5 }}
          >
            Browse, filter, and expand your saved meals
          </Typography>
        </Box>
      )}

      <TextField
        size="small"
        label="Filter by title"
        value={filterText}
        onChange={(e) => onFilterChange(e.target.value)}
        sx={{
          minWidth: { xs: "100%", sm: 260 },
          "& .MuiOutlinedInput-root": {
            borderRadius: "14px",
            backgroundColor: colors.white,
            "& fieldset": {
              borderColor: colors.border,
            },
            "&:hover fieldset": {
              borderColor: colors.green,
            },
            "&.Mui-focused fieldset": {
              borderColor: colors.green,
              borderWidth: 2,
            },
          },
          "& .MuiInputLabel-root.Mui-focused": {
            color: colors.green,
          },
        }}
      />
    </Toolbar>
  );
}

EnhancedTableToolbar.propTypes = {
  filterText: PropTypes.string.isRequired,
  numSelected: PropTypes.number.isRequired,
  onFilterChange: PropTypes.func.isRequired,
};

function RecipeDetailsRow({ recipe, open, colSpan }) {
  const cookTime = recipe.cook_time ?? recipe.cookingTimeMinutes ?? "—";

  return (
    <TableRow>
      <TableCell
        colSpan={colSpan}
        sx={{
          py: 0,
          borderBottom: `1px solid ${colors.border}`,
          backgroundColor: colors.white,
        }}
      >
        <Collapse in={open} timeout="auto" unmountOnExit>
          <Box
            sx={{
              m: 2,
              p: 2.5,
              borderRadius: "18px",
              background: `linear-gradient(180deg, ${colors.orangeSoft} 0%, ${colors.white} 100%)`,
              border: `1px solid ${alpha(colors.orange, 0.12)}`,
            }}
          >
            <Typography
              variant="subtitle1"
              sx={{
                mb: 1.5,
                fontWeight: 800,
                color: colors.textPrimary,
              }}
            >
              Recipe Details
            </Typography>

            <Box
              sx={{
                display: "inline-flex",
                alignItems: "center",
                px: 1.5,
                py: 0.75,
                mb: 2,
                borderRadius: "999px",
                backgroundColor: alpha(colors.orange, 0.12),
                color: colors.orange,
                fontWeight: 700,
                fontSize: "0.92rem",
              }}
            >
              Cook Time: {cookTime} min
            </Box>

            <Typography
              sx={{
                mb: 1,
                color: colors.textPrimary,
                lineHeight: 1.7,
              }}
            >
              <Box component="span" sx={{ fontWeight: 700 }}>
                Instructions:
              </Box>{" "}
              {recipe.instructions || "—"}
            </Typography>

            <Typography
              variant="subtitle2"
              sx={{
                mt: 2.5,
                mb: 1,
                fontWeight: 800,
                color: colors.green,
              }}
            >
              Ingredients
            </Typography>

            {recipe.ingredients?.length ? (
              <Box
                component="ul"
                sx={{
                  pl: 3,
                  m: 0,
                  color: colors.textPrimary,
                  "& li": {
                    mb: 0.75,
                    lineHeight: 1.6,
                  },
                }}
              >
                {recipe.ingredients.map((ingredient, index) => (
                  <li key={index}>
                    {ingredient.name} — {ingredient.quantity} {ingredient.unit}
                  </li>
                ))}
              </Box>
            ) : (
              <Typography sx={{ color: colors.textSecondary }}>
                No ingredients listed.
              </Typography>
            )}
          </Box>
        </Collapse>
      </TableCell>
    </TableRow>
  );
}

RecipeDetailsRow.propTypes = {
  open: PropTypes.bool.isRequired,
  recipe: PropTypes.object.isRequired,
  colSpan: PropTypes.number,
};

RecipeDetailsRow.defaultProps = {
  colSpan: 4,
};

export default function SavedRecipesTable({
  recipes = [],
  onDeleteRecipe,
  deletingRecipeId = null,
}) {
  const [order, setOrder] = React.useState("asc");
  const [orderBy, setOrderBy] = React.useState("title");
  const [selected, setSelected] = React.useState([]);
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);
  const [filterText, setFilterText] = React.useState("");
  const [openRows, setOpenRows] = React.useState({});

  const normalizedRecipes = React.useMemo(
    () =>
      recipes.map((recipe, index) => ({
        ...recipe,
        _rowId: recipe.id ?? `${recipe.title ?? "recipe"}-${index}`,
      })),
    [recipes]
  );

  const filteredRecipes = React.useMemo(() => {
    const query = filterText.trim().toLowerCase();
    if (!query) return normalizedRecipes;

    return normalizedRecipes.filter((recipe) =>
      (recipe.title ?? "").toLowerCase().includes(query)
    );
  }, [normalizedRecipes, filterText]);

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleSelectAllClick = (event) => {
    if (event.target.checked) {
      const newSelected = filteredRecipes.map((n) => n._rowId);
      setSelected(newSelected);
      return;
    }
    setSelected([]);
  };

  const handleClick = (event, id) => {
    event.stopPropagation();

    const selectedIndex = selected.indexOf(id);
    let newSelected = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, id);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      );
    }

    setSelected(newSelected);
  };

  const handleToggleRow = (rowId) => {
    setOpenRows((prev) => ({
      ...prev,
      [rowId]: !prev[rowId],
    }));
  };

  const handleDeleteRecipe = async (event, recipe) => {
    event.stopPropagation();

    if (!onDeleteRecipe) return;

    await onDeleteRecipe(recipe);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const sortedRecipes = React.useMemo(
    () => [...filteredRecipes].sort(getComparator(order, orderBy)),
    [filteredRecipes, order, orderBy]
  );

  const visibleRows = React.useMemo(
    () =>
      sortedRecipes.slice(
        page * rowsPerPage,
        page * rowsPerPage + rowsPerPage
      ),
    [sortedRecipes, page, rowsPerPage]
  );

  if (!recipes.length) {
    return (
      <Paper
        elevation={0}
        sx={{
          p: 3,
          borderRadius: "24px",
          border: `1px solid ${colors.border}`,
          backgroundColor: colors.white,
        }}
      >
        <Typography sx={{ color: colors.textSecondary }}>
          No saved recipes.
        </Typography>
      </Paper>
    );
  }

  return (
    <Box sx={{ width: "100%" }}>
      <Paper
        elevation={0}
        sx={{
          width: "100%",
          mb: 2,
          borderRadius: "24px",
          overflow: "hidden",
          border: `1px solid ${colors.border}`,
          backgroundColor: colors.white,
          boxShadow: "0 10px 30px rgba(0,0,0,0.04)",
        }}
      >
        <EnhancedTableToolbar
          numSelected={selected.length}
          filterText={filterText}
          onFilterChange={setFilterText}
        />

        <TableContainer>
          <Table aria-labelledby="tableTitle">
            <EnhancedTableHead
              numSelected={selected.length}
              order={order}
              orderBy={orderBy}
              onSelectAllClick={handleSelectAllClick}
              onRequestSort={handleRequestSort}
              rowCount={filteredRecipes.length}
            />

            <TableBody>
              {visibleRows.map((recipe, index) => {
                const isItemSelected = selected.includes(recipe._rowId);
                const isOpen = !!openRows[recipe._rowId];
                const labelId = `saved-recipe-checkbox-${index}`;
                const isAltRow = index % 2 === 1;
                const isDeleting = deletingRecipeId === recipe.id;

                return (
                  <React.Fragment key={recipe._rowId}>
                    <TableRow
                      hover
                      selected={isItemSelected}
                      sx={{
                        cursor: "pointer",
                        backgroundColor: isItemSelected
                          ? alpha(colors.green, 0.12)
                          : isAltRow
                            ? colors.rowAlt
                            : colors.white,
                        transition: "background-color 0.2s ease",
                        "&:hover": {
                          backgroundColor: isItemSelected
                            ? alpha(colors.green, 0.16)
                            : colors.greenHover,
                        },
                        "& td, & th": {
                          borderBottom: isOpen
                            ? "none"
                            : `1px solid ${colors.border}`,
                        },
                      }}
                      onClick={() => handleToggleRow(recipe._rowId)}
                    >
                      <TableCell sx={{ width: 64 }}>
                        <IconButton
                          aria-label={
                            isOpen ? "collapse recipe row" : "expand recipe row"
                          }
                          size="small"
                          onClick={(event) => {
                            event.stopPropagation();
                            handleToggleRow(recipe._rowId);
                          }}
                          sx={{
                            border: `1px solid ${alpha(colors.green, 0.2)}`,
                            backgroundColor: isOpen
                              ? alpha(colors.green, 0.12)
                              : colors.white,
                            color: isOpen ? colors.green : colors.textSecondary,
                            transition: "all 0.2s ease",
                            "&:hover": {
                              backgroundColor: alpha(colors.orange, 0.12),
                              color: colors.orange,
                              borderColor: alpha(colors.orange, 0.25),
                            },
                          }}
                        >
                          {isOpen ? (
                            <KeyboardArrowUpIcon />
                          ) : (
                            <KeyboardArrowDownIcon />
                          )}
                        </IconButton>
                      </TableCell>

                      <TableCell padding="checkbox">
                        <Checkbox
                          color="default"
                          checked={isItemSelected}
                          onClick={(event) => handleClick(event, recipe._rowId)}
                          sx={{
                            color: colors.green,
                            "&.Mui-checked": {
                              color: colors.green,
                            },
                          }}
                        />
                      </TableCell>

                      <TableCell
                        component="th"
                        id={labelId}
                        scope="row"
                        padding="none"
                        sx={{
                          py: 2.25,
                          fontWeight: 700,
                          color: colors.textPrimary,
                          fontSize: "0.98rem",
                        }}
                      >
                        {recipe.title}
                      </TableCell>

                      <TableCell align="right" sx={{ pr: 3 }}>
                        <Button
                          variant="outlined"
                          color="error"
                          size="small"
                          startIcon={<DeleteOutlineIcon />}
                          onClick={(event) => handleDeleteRecipe(event, recipe)}
                          disabled={isDeleting}
                          sx={{
                            borderRadius: "12px",
                            textTransform: "none",
                            fontWeight: 700,
                          }}
                        >
                          {isDeleting ? "Deleting..." : "Delete"}
                        </Button>
                      </TableCell>
                    </TableRow>

                    <RecipeDetailsRow recipe={recipe} open={isOpen} colSpan={4} />
                  </React.Fragment>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>

        <TablePagination
          rowsPerPageOptions={[10, 20, 30]}
          component="div"
          count={filteredRecipes.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          sx={{
            borderTop: `1px solid ${colors.border}`,
            backgroundColor: "#FCFCFC",
            "& .MuiTablePagination-selectLabel, & .MuiTablePagination-displayedRows":
              {
                color: colors.textSecondary,
                fontWeight: 500,
              },
            "& .MuiIconButton-root": {
              color: colors.green,
            },
          }}
        />
      </Paper>
    </Box>
  );
}

SavedRecipesTable.propTypes = {
  recipes: PropTypes.array,
  onDeleteRecipe: PropTypes.func,
  deletingRecipeId: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
};

SavedRecipesTable.defaultProps = {
  onDeleteRecipe: undefined,
  deletingRecipeId: null,
};