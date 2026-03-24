import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import RegisterPage from "../RegisterPage";

const mockNavigate = vi.fn();

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe("RegisterPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch = vi.fn();
  });

  const renderPage = () => {
    return render(
      <MemoryRouter>
        <RegisterPage />
      </MemoryRouter>
    );
  };

  it("renders all form fields", () => {
    renderPage();

    expect(screen.getByLabelText(/First Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Last Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
  });

  it("shows validation errors when submitting empty form", async () => {
    renderPage();

    fireEvent.submit(screen.getByRole("form"));

    expect(await screen.findByText(/First name is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/Last name is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/Email is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/Password is required/i)).toBeInTheDocument();
  });

  it("enables submit button when form is valid", () => {
    renderPage();

    fireEvent.change(screen.getByLabelText(/First Name/i), {
      target: { value: "Justin" },
    });

    fireEvent.change(screen.getByLabelText(/Last Name/i), {
      target: { value: "McLinn" },
    });

    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: "test@email.com" },
    });

    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: "Password1" },
    });

    const button = screen.getByRole("button", { name: /Create Account/i });

    expect(button).not.toBeDisabled();
  });

  it("calls backend and navigates on successful submit", async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            id: 1,
            username: "test@email.com",
            email: "test@email.com",
          }),
      })
    );

    renderPage();

    fireEvent.change(screen.getByLabelText(/First Name/i), {
      target: { value: "Justin" },
    });

    fireEvent.change(screen.getByLabelText(/Last Name/i), {
      target: { value: "McLinn" },
    });

    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: "test@email.com" },
    });

    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: "Password1" },
    });

    fireEvent.click(screen.getByRole("button", { name: /Create Account/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        "/api/user/register",
        expect.objectContaining({
          method: "POST",
        })
      );
    });

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith("/login");
    });
  });

  it("shows error message when API fails", async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: false,
        json: () =>
          Promise.resolve({
            detail: "User already exists",
          }),
      })
    );

    renderPage();

    fireEvent.change(screen.getByLabelText(/First Name/i), {
      target: { value: "Justin" },
    });

    fireEvent.change(screen.getByLabelText(/Last Name/i), {
      target: { value: "McLinn" },
    });

    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: "test@email.com" },
    });

    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: "Password1" },
    });

    fireEvent.click(screen.getByRole("button", { name: /Create Account/i }));

    expect(await screen.findByText(/User already exists/i)).toBeInTheDocument();
  });
});