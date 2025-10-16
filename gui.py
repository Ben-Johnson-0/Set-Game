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

        # Build UI
        self.card_images = []
        self.card_buttons = []

        self.create_widgets()
        self.render_cards()

    def create_widgets(self):
        """Creates and Packs basic menu/control buttons"""
        self.card_frame = tk.Frame(self, bg="#f5f5f5")
        self.card_frame.pack(padx=20, pady=20)

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
                messagebox.showinfo("Set Found!", "That's a valid Set!")
            else:
                messagebox.showwarning("Not a Set", f"That combination is not valid.\n{self.game.board[self.game.selected]}")

        self.render_cards()

    def new_game(self):
        self.game = SetGame()
        self.render_cards()

    def show_hint(self):
        isFound, hint, _ = self.game.find_set()
        if isFound:
            messagebox.showinfo("Hint", f"Possible set at indices: {hint}")
        else:
            messagebox.showinfo("Hint", "No sets available!")

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    app = SetGUI()
    app.mainloop()
