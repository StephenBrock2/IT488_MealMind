import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import CreateRecipeDialog from "../CreateRecipeDialog";

describe("CreateRecipeDialog", () => {
  const onClose = vi.fn();
  const onCreate = vi.fn();

  beforeEach(() => {
    onClose.mockClear();
    onCreate.mockClear();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  function renderOpen() {
    return render(<CreateRecipeDialog open={true} onClose={onClose} onCreate={onCreate} />);
  }

  it("disables Save until required fields are filled", async () => {
    renderOpen();

    const saveBtn = screen.getByRole("button", { name: /save/i });
    expect(saveBtn).toBeDisabled();

    await userEvent.type(screen.getByLabelText(/title/i), "My Recipe");
    expect(saveBtn).toBeDisabled(); 

    await userEvent.type(screen.getByLabelText(/cooking time/i), "10");
    expect(saveBtn).toBeDisabled();

    await userEvent.type(screen.getByLabelText(/^name$/i), "ground beef");
    expect(saveBtn).toBeDisabled();

    await userEvent.type(screen.getByLabelText(/^qty$/i), "1");
    expect(saveBtn).toBeDisabled();

    await userEvent.type(screen.getByLabelText(/^unit$/i), "lb");
    expect(saveBtn).toBeDisabled();

    await userEvent.type(screen.getByLabelText(/instructions/i), "Cook it.");
    expect(saveBtn).toBeEnabled();
  });

  it("adds an ingredient row when clicking Add", async () => {
    renderOpen();


    expect(screen.getAllByLabelText(/^name$/i)).toHaveLength(1);

    await userEvent.click(screen.getByRole("button", { name: /add/i }));


    expect(screen.getAllByLabelText(/^name$/i)).toHaveLength(2);
  });

  it("submits structured payload, posts to backend, and closes on success", async () => {

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ ok: true }),
    });
    vi.stubGlobal("fetch", fetchMock);

    renderOpen();

    await userEvent.type(screen.getByLabelText(/title/i), "Spaghetti");
    await userEvent.type(screen.getByLabelText(/cooking time/i), "45");
    await userEvent.type(screen.getByLabelText(/^name$/i), "ground beef");
    await userEvent.type(screen.getByLabelText(/^qty$/i), "1");
    await userEvent.type(screen.getByLabelText(/^unit$/i), "lb");
    await userEvent.type(screen.getByLabelText(/instructions/i), "Brown beef, simmer sauce.");

    await userEvent.click(screen.getByRole("button", { name: /^save$/i }));

    await waitFor(() => {
      expect(onCreate).toHaveBeenCalledTimes(1);
    });

    const payload = onCreate.mock.calls[0][0];
    expect(payload).toEqual({
      title: "Spaghetti",
      instructions: "Brown beef, simmer sauce.",
      cookingTimeMinutes: 45,
      ingredients: [{ name: "ground beef", quantity: 1, unit: "lb" }],
    });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, options] = fetchMock.mock.calls[0];
    expect(url).toBe("/api/recipe");
    expect(options.method).toBe("POST");
    expect(options.headers).toEqual({ "Content-Type": "application/json" });

    const bodyObj = JSON.parse(options.body);
    expect(bodyObj).toEqual(payload);

    await waitFor(() => {
      expect(onClose).toHaveBeenCalledTimes(1);
    });
  });

  it("shows an error if backend returns non-OK", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 405,
      json: async () => ({ detail: "Method Not Allowed" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    renderOpen();

    await userEvent.type(screen.getByLabelText(/title/i), "Test");
    await userEvent.type(screen.getByLabelText(/cooking time/i), "10");
    await userEvent.type(screen.getByLabelText(/^name$/i), "tomato");
    await userEvent.type(screen.getByLabelText(/^qty$/i), "1");
    await userEvent.type(screen.getByLabelText(/^unit$/i), "whole");
    await userEvent.type(screen.getByLabelText(/instructions/i), "Do stuff.");

    await userEvent.click(screen.getByRole("button", { name: /^save$/i }));

    expect(await screen.findByText(/method not allowed/i)).toBeInTheDocument();

    expect(onClose).not.toHaveBeenCalled();
  });
});