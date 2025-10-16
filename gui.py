import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
from set import SetGame
from card_renderer import CardRenderer

CARD_SPACING = 20
CARDS_PER_ROW = 4


class SetGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Set Game")
        self.configure(bg="#f5f5f5")

        self.renderer = CardRenderer()
        self.game = SetGame()

        # Game Vars
        self.matches_var = tk.IntVar(value=self.game.matches)
        self.score_var = tk.IntVar(value=0)
        self.hints_var = tk.IntVar(value=0)

        # Build UI
        self.card_images = []
        self.card_buttons = []

        self.create_widgets()
        self.render_cards()


    def create_widgets(self):
        """Creates and Packs basic menu/control buttons"""
        self.card_frame = tk.Frame(self, bg="#f5f5f5")
        self.card_frame.pack(padx=20, pady=20)

        # Score label
        score_frame = tk.Frame(self, bg="#f5f5f5")
        score_frame.pack(pady=(0, 5))
        tk.Label(score_frame, text="Score:", width=12, bg="#f5f5f5").pack(side=tk.LEFT)
        tk.Label(score_frame, textvariable=self.score_var, bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        tk.Label(score_frame, text="Sets Found:", width=12, bg="#f5f5f5").pack(side=tk.LEFT)
        tk.Label(score_frame, textvariable=self.matches_var, bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        tk.Label(score_frame, text="Hints Used:", width=12, bg="#f5f5f5").pack(side=tk.LEFT)
        tk.Label(score_frame, textvariable=self.hints_var, bg="#f5f5f5").pack(side=tk.LEFT, padx=5)

        # Control buttons
        controls = tk.Frame(self, bg="#f5f5f5")
        controls.pack()

        tk.Button(controls, text="New Game", command=self.new_game, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Hint", command=self.show_hint, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Quit", command=self.quit, width=12).pack(side=tk.LEFT, padx=5)

    # -------------------------------
    # Rendering
    # -------------------------------
    def render_cards(self):
        """Render the current cards as clickable tkinter canvases."""
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        cards = self.game.board
        for idx, card in enumerate(cards):
            img = self.renderer.render_card(tuple(card))
            tk_img = ImageTk.PhotoImage(img)
            self.card_images.append(tk_img)

            btn = tk.Button(self.card_frame, image=tk_img, command=lambda i=idx: self.toggle_card(i), bg=self.card_color(idx), highlightthickness=5)
            btn.grid(row=idx//CARDS_PER_ROW, column=idx%CARDS_PER_ROW, padx=5, pady=5)
            self.card_buttons.append(btn)

    def card_color(self, idx):
        """Highlight selected cards."""
        return "#b2fab4" if idx in self.game.selected else "white"

    # -------------------------------
    # Game Interaction & Control Functions
    # -------------------------------
    def toggle_card(self, idx):
        self.game.select_card(idx)
        self.render_cards()

        # Once 3 selected, check if they form a set
        if len(self.game.selected) == 3:
            result : bool = self.game.submit_selection()
            if result:
                self.matches_var.set(self.game.matches)
                self.score_var.set(self.matches_var.get() - self.hints_var.get())
            else:
                messagebox.showwarning("Not a Set", f"That combination is not valid.\n{self.game.board[self.game.selected]}")

        self.render_cards()

    def new_game(self):
        self.game = SetGame()
        self.matches_var.set(self.game.matches)
        self.render_cards()

    def show_hint(self):
        isFound, hint, _ = self.game.find_set()
        if isFound:
            self.hints_var.set(self.hints_var.get() + 1)
            self.score_var.set(self.matches_var.get() - self.hints_var.get())
            messagebox.showinfo("Hint", f"Possible set at indices: {hint}")
        else:
            messagebox.showinfo("Hint", "No sets available!")

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    app = SetGUI()
    app.mainloop()
