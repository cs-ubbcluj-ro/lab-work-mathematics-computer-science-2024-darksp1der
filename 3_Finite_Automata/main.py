import tkinter as tk


class FiniteAutomaton:
    def __init__(self, file_path):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.final_states = set()
        self.read_from_file(file_path)

    def read_from_file(self, file_path):

        with open(file_path, 'r') as file:
            lines = file.readlines()

        self.states = set(lines[0].strip().split(","))
        self.alphabet = set(lines[1].strip().split(","))
        self.initial_state = lines[2].strip()
        self.final_states = set(lines[3].strip().split(","))
        for line in lines[4:]:
            parts = line.strip().split("->")
            left = parts[0].strip()
            right = parts[1].strip()
            state, symbol = left.split(",")
            state = state.strip()
            symbol = symbol.strip()
            next_state = right
            if (state, symbol) not in self.transitions:
                self.transitions[(state, symbol)] = []
            self.transitions[(state, symbol)].append(next_state)

    def is_valid_token(self, string):

        current_states = [self.initial_state]
        for symbol in string:
            next_states = []
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.extend(self.transitions[(state, symbol)])
            current_states = next_states

        return any(state in self.final_states for state in current_states)

    def is_deterministic(self):

        for (state, symbol), next_states in self.transitions.items():
            if len(next_states) > 1:
                return False  # More than one transition for the same symbol in the same state
        return True

    def display(self, root):

        display_frame = tk.Frame(root)
        display_frame.pack(padx=10, pady=10)

        tk.Label(display_frame, text="=== Finite Automaton Description ===", font=("Arial", 14, "bold")).grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=2,
                                                                                                              pady=5)

        tk.Label(display_frame, text="1. Set of States:").grid(row=1, column=0, sticky="w")
        tk.Label(display_frame, text=f"{', '.join(self.states)}").grid(row=1, column=1, sticky="w")

        tk.Label(display_frame, text="2. Alphabet (Symbols):").grid(row=2, column=0, sticky="w")
        tk.Label(display_frame, text=f"{', '.join(self.alphabet)}").grid(row=2, column=1, sticky="w")

        tk.Label(display_frame, text="3. Transitions:").grid(row=3, column=0, sticky="w")
        row_idx = 4
        for key, value in self.transitions.items():
            for target in value:
                transition_text = f"δ({key[0]}, {key[1]}) -> {target}"
                tk.Label(display_frame, text=transition_text).grid(row=row_idx, column=0, columnspan=2, sticky="w")
                row_idx += 1

        tk.Label(display_frame, text="4. Initial State:").grid(row=row_idx, column=0, sticky="w")
        tk.Label(display_frame, text=self.initial_state).grid(row=row_idx, column=1, sticky="w")
        row_idx += 1

        tk.Label(display_frame, text="5. Final States:").grid(row=row_idx, column=0, sticky="w")
        tk.Label(display_frame, text=f"{', '.join(self.final_states)}").grid(row=row_idx, column=1, sticky="w")

    def validate_input(self, input_string, result_label):

        if self.is_valid_token(input_string):
            result_label.config(text=f"'{input_string}' is a valid lexical token.", fg="green")
        else:
            result_label.config(text=f"'{input_string}' is NOT a valid lexical token.", fg="red")

    def display_determinism(self, result_label):

        if self.is_deterministic():
            result_label.config(text="The automaton is deterministic.", fg="green")
        else:
            result_label.config(text="The automaton is NOT deterministic.", fg="red")


def main():
    fa = FiniteAutomaton("FA.in")

    root = tk.Tk()
    root.title("Finite Automaton Validator")

    fa.display(root)

    tk.Label(root, text="Enter a string to check if it is a valid lexical token:").pack(padx=10, pady=10)

    input_entry = tk.Entry(root, width=30)
    input_entry.pack(padx=10, pady=5)

    result_label = tk.Label(root, text="", font=("Arial", 12))
    result_label.pack(padx=10, pady=10)

    validate_button = tk.Button(root, text="Validate Token", command=lambda: fa.validate_input(input_entry.get(), result_label))
    validate_button.pack(padx=10, pady=5)

    determinism_button = tk.Button(root, text="Check Determinism", command=lambda: fa.display_determinism(result_label))
    determinism_button.pack(padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()