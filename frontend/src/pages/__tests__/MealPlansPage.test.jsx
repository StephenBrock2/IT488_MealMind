import {
  describe,
  it,
  expect,
  vi,
  beforeEach,
  afterEach,
} from "vitest";
import {
  render,
  screen,
  waitFor,
  cleanup,
  fireEvent,
} from "@testing-library/react";
import MealPlansPage from "../MealPlansPage";

vi.mock("../../components/Header", () => ({
  default: () => <div data-testid="header" />,
}));

vi.mock("../../components/RecipeSelectDialog", () => ({
  default: ({ open, recipes = [], loading, onClose, onSelect }) =>
    open ? (
      <div data-testid="recipe-select-dialog">
        <div>Recipe Dialog</div>
        {loading ? (
          <div>Loading...</div>
        ) : (
          recipes.map((recipe) => (
            <button key={recipe.id} onClick={() => onSelect(recipe)}>
              Choose {recipe.title}
            </button>
          ))
        )}
        <button onClick={onClose}>Close Dialog</button>
      </div>
    ) : null,
}));

function mockFetchSequence(...responses) {
  global.fetch = vi.fn();
  responses.forEach((response) => {
    global.fetch.mockResolvedValueOnce(response);
  });
}

function jsonResponse(data, ok = true, status = 200) {
  return {
    ok,
    status,
    json: vi.fn().mockResolvedValue(data),
  };
}

describe("MealPlansPage", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    global.fetch = vi.fn();
  });

  afterEach(() => {
    cleanup();
  });

  it("fetches recipes and meal plans on initial load", async () => {
    mockFetchSequence(jsonResponse([]), jsonResponse({}));

    render(<MealPlansPage />);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(2);
    });

    expect(global.fetch).toHaveBeenNthCalledWith(1, "/api/recipe_list", {
      credentials: "include",
    });

    expect(global.fetch).toHaveBeenNthCalledWith(2, "/api/meal_plan", {
      credentials: "include",
    });
  });

  it("renders meal planner heading and default week view", async () => {
    mockFetchSequence(jsonResponse([]), jsonResponse({}));

    render(<MealPlansPage />);

    expect(
      screen.getByRole("heading", { name: /meal planner/i })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: /week view/i })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: /day view/i })
    ).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getAllByText(/breakfast/i).length).toBeGreaterThan(0);
    });
  });

  it("switches from week view to day view", async () => {
    mockFetchSequence(jsonResponse([]), jsonResponse({}));

    render(<MealPlansPage />);

    await waitFor(() => {
      expect(screen.getAllByText(/breakfast/i).length).toBeGreaterThan(1);
    });

    fireEvent.click(screen.getByRole("button", { name: /day view/i }));

    await waitFor(() => {
      expect(screen.getAllByText(/breakfast/i)).toHaveLength(1);
    });
  });

  it("opens the recipe dialog when Add Recipe is clicked", async () => {
    mockFetchSequence(
      jsonResponse([{ id: 1, title: "Chicken Alfredo", cook_time: 20 }]),
      jsonResponse({})
    );

    render(<MealPlansPage />);

    const addButtons = await screen.findAllByRole("button", {
      name: /add recipe/i,
    });

    fireEvent.click(addButtons[0]);

    expect(
      screen.getByTestId("recipe-select-dialog")
    ).toBeInTheDocument();
  });

  it("assigns a selected recipe to a slot and shows unsaved changes", async () => {
    mockFetchSequence(
      jsonResponse([{ id: 1, title: "Chicken Alfredo", cook_time: 20 }]),
      jsonResponse({})
    );

    render(<MealPlansPage />);

    const addButtons = await screen.findAllByRole("button", {
      name: /add recipe/i,
    });

    fireEvent.click(addButtons[0]);
    fireEvent.click(
      screen.getByRole("button", { name: /choose chicken alfredo/i })
    );

    expect(await screen.findByText("Chicken Alfredo")).toBeInTheDocument();
    expect(screen.getByText(/unsaved changes/i)).toBeInTheDocument();
  });

  it("removes a selected recipe from a slot", async () => {
    mockFetchSequence(
      jsonResponse([{ id: 1, title: "Chicken Alfredo", cook_time: 20 }]),
      jsonResponse({})
    );

    render(<MealPlansPage />);

    const addButtons = await screen.findAllByRole("button", {
      name: /add recipe/i,
    });

    fireEvent.click(addButtons[0]);
    fireEvent.click(
      screen.getByRole("button", { name: /choose chicken alfredo/i })
    );

    expect(await screen.findByText("Chicken Alfredo")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /remove/i }));

    await waitFor(() => {
      expect(screen.queryByText("Chicken Alfredo")).not.toBeInTheDocument();
    });
  });

  it("hydrates and displays a saved meal plan from backend response", async () => {
    mockFetchSequence(
      jsonResponse([
        { id: 2, title: "Tacos", cook_time: 15 },
        { id: 5, title: "Spaghetti", cook_time: 30 },
      ]),
      jsonResponse({
        "1": {
          "2026-03-30": {
            breakfast: null,
            lunch: 2,
            dinner: null,
          },
        },
      })
    );

    render(<MealPlansPage />);

    expect(await screen.findByText("Tacos")).toBeInTheDocument();
    expect(screen.getByText(/cook time: 15 min/i)).toBeInTheDocument();
  });

  it("uses the latest meal plan entry when multiple saved plans exist", async () => {
    mockFetchSequence(
      jsonResponse([
        { id: 2, title: "Tacos", cook_time: 15 },
        { id: 5, title: "Spaghetti", cook_time: 30 },
      ]),
      jsonResponse({
        "1": {
          "2026-03-30": {
            breakfast: null,
            lunch: 2,
            dinner: null,
          },
        },
        "2": {
          "2026-03-30": {
            breakfast: null,
            lunch: 5,
            dinner: null,
          },
        },
      })
    );

    render(<MealPlansPage />);

    expect(await screen.findByText("Spaghetti")).toBeInTheDocument();
    expect(screen.queryByText("Tacos")).not.toBeInTheDocument();
  });

  it("saves meal plan with the correct payload", async () => {
    mockFetchSequence(
      jsonResponse([{ id: 1, title: "Chicken Alfredo", cook_time: 20 }]),
      jsonResponse({}),
      jsonResponse({ message: "Meal plan saved successfully" })
    );

    render(<MealPlansPage />);

    const addButtons = await screen.findAllByRole("button", {
      name: /add recipe/i,
    });

    fireEvent.click(addButtons[0]);
    fireEvent.click(
      screen.getByRole("button", { name: /choose chicken alfredo/i })
    );

    fireEvent.click(screen.getByRole("button", { name: /save plan/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(3);
    });

    const saveCall = global.fetch.mock.calls[2];
    expect(saveCall[0]).toBe("/api/meal_plan");
    expect(saveCall[1]).toEqual({
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: expect.any(String),
    });

    const parsedBody = JSON.parse(saveCall[1].body);

    expect(Object.keys(parsedBody.plans).length).toBe(1);

    const firstDate = Object.keys(parsedBody.plans)[0];
    expect(parsedBody.plans[firstDate]).toEqual({
      breakfast: 1,
      lunch: null,
      dinner: null,
    });
  });

  it("shows success message after saving", async () => {
    mockFetchSequence(
      jsonResponse([{ id: 1, title: "Chicken Alfredo", cook_time: 20 }]),
      jsonResponse({}),
      jsonResponse({ message: "Meal plan saved successfully" })
    );

    render(<MealPlansPage />);

    const addButtons = await screen.findAllByRole("button", {
      name: /add recipe/i,
    });

    fireEvent.click(addButtons[0]);
    fireEvent.click(
      screen.getByRole("button", { name: /choose chicken alfredo/i })
    );
    fireEvent.click(screen.getByRole("button", { name: /save plan/i }));

    expect(await screen.findByText(/meal plan saved\./i)).toBeInTheDocument();
  });

  it("shows failure message if save fails", async () => {
    mockFetchSequence(
      jsonResponse([{ id: 1, title: "Chicken Alfredo", cook_time: 20 }]),
      jsonResponse({}),
      jsonResponse({}, false, 500)
    );

    render(<MealPlansPage />);

    const addButtons = await screen.findAllByRole("button", {
      name: /add recipe/i,
    });

    fireEvent.click(addButtons[0]);
    fireEvent.click(
      screen.getByRole("button", { name: /choose chicken alfredo/i })
    );
    fireEvent.click(screen.getByRole("button", { name: /save plan/i }));

    expect(
      await screen.findByText(/could not save meal plan\./i)
    ).toBeInTheDocument();
  });

  it("shows no saved plan when meal plan request returns 401", async () => {
    mockFetchSequence(
      jsonResponse([{ id: 1, title: "Chicken Alfredo", cook_time: 20 }]),
      jsonResponse({}, false, 401)
    );

    render(<MealPlansPage />);

    await waitFor(() => {
      expect(screen.queryByText("Chicken Alfredo")).not.toBeInTheDocument();
    });
  });
});