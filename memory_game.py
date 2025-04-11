import tkinter as tk
import random
import winsound

emoji_pool = [
    '🐶','🐱','🐼','🦁','🐵','🐸','🐷','🐰','🐢','🐍','🦊','🐯','🐨',
    '🍎','🍌','🍇','🍉','🍓','🍍','🍑','🥝','🍒','🍐',
    '🦉','🐦','🦜','🐧','🐝','🐞',
    '🚗','🚕','🚙','🚌','🚓','🚑','🚒','🚜','🚲','✈️','🚂','🚁'
]

selected_emojis = random.sample(emoji_pool, 25)
cards = selected_emojis * 2
random.shuffle(cards)

buttons = []
flipped = []
matched = set()
player_turn = 1
score = {1: 0, 2: 0}
lock = False

BG_COLOR = "#f0f4ff"
BTN_COLOR = "#cde3ff"
BTN_FLIPPED = "#ffffff"
BTN_MATCHED = "#d4edda"
SCORE_BG = "#d1e7dd"
FONT_BIG = ("Arial", 24)
FONT_HEADER = ("Helvetica", 16, "bold")
FONT_SCORE = ("Helvetica", 14)

root = tk.Tk()
root.title("🧠 Emoji Memory Match")
root.configure(bg=BG_COLOR)

score_frame = tk.Frame(root, bg=SCORE_BG, bd=2, relief="ridge", padx=10, pady=5)
score_frame.pack(pady=10)

turn_label = tk.Label(score_frame, text="Player 1's Turn", font=FONT_HEADER, bg=SCORE_BG)
turn_label.grid(row=0, column=0, columnspan=5, pady=5)

score_label = tk.Label(score_frame, text="Score - Player 1: 0 | Player 2: 0", font=FONT_SCORE, bg=SCORE_BG)
score_label.grid(row=1, column=0, columnspan=5, pady=5)

def update_ui():
    turn_label.config(text=f"Player {player_turn}'s Turn")
    score_label.config(text=f"Score - Player 1: {score[1]} | Player 2: {score[2]}")

def check_match():
    global flipped, matched, player_turn, score, lock

    i, j = flipped
    if cards[i] == cards[j]:
        matched.update([i, j])
        score[player_turn] += 1
        buttons[i].config(bg=BTN_MATCHED, state="disabled")
        buttons[j].config(bg=BTN_MATCHED, state="disabled")
        winsound.MessageBeep(winsound.MB_OK)
    else:
        buttons[i].config(text="❓", bg=BTN_COLOR, state="normal")
        buttons[j].config(text="❓", bg=BTN_COLOR, state="normal")
        player_turn = 2 if player_turn == 1 else 1

    flipped.clear()
    lock = False
    update_ui()

    if len(matched) == len(cards):
        winner = "🎉 It's a tie!"
        if score[1] > score[2]:
            winner = "🏆 Player 1 Wins!"
        elif score[2] > score[1]:
            winner = "🏆 Player 2 Wins!"
        turn_label.config(text=winner)

def flip_card(i):
    global lock
    if lock or i in matched or i in flipped:
        return

    buttons[i].config(text=cards[i], bg=BTN_FLIPPED, state="disabled")
    flipped.append(i)

    if len(flipped) == 2:
        lock = True
        root.after(700, check_match)

card_frame = tk.Frame(root, bg=BG_COLOR)
card_frame.pack(pady=10)

for i in range(50):
    btn = tk.Button(card_frame, text="❓", width=4, height=2,
                    font=FONT_BIG, bg=BTN_COLOR, activebackground=BTN_COLOR,
                    command=lambda i=i: flip_card(i))
    btn.grid(row=i//10, column=i%10, padx=4, pady=4)
    buttons.append(btn)

root.mainloop()
