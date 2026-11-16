/-!
Erdős Problem #160: a 7-colouring of {1, …, 77} in which every 4-term arithmetic progression receives at least
three distinct colours. Positions are 0-indexed here (position i stands for the integer i + 1).
Core Lean only; the proof is `decide` (kernel evaluation), no `native_decide`.
-/

/-- The colouring: colour of the integer i + 1, for i = 0, …, 76. -/
def colouring : List Nat := [1,1,6,2,1,1,0,4,4,6,3,5,3,4,5,2,1,2,0,3,3,4,2,2,5,0,5,6,6,0,4,3,4,6,3,1,5,1,3,5,2,0,2,1,1,0,4,2,2,5,4,5,6,6,0,4,1,4,6,3,1,5,0,4,0,3,3,1,2,6,2,1,6,2,5,2,0]

/-- Colour of position i (0-indexed). -/
def col (i : Nat) : Nat := colouring.getD i 0

/-- Number of distinct values among four natural numbers. -/
def ndistinct (a b c d : Nat) : Nat :=
  1 + (if b ≠ a then 1 else 0) + (if c ≠ a ∧ c ≠ b then 1 else 0) + (if d ≠ a ∧ d ≠ b ∧ d ≠ c then 1 else 0)

theorem colouring_length : colouring.length = 77 := by decide

theorem colours_lt_seven : ∀ i, i < 77 → col i < 7 := by decide

/-- Every 4-term progression a, a+d, a+2d, a+3d inside {0, …, 76} with d ≥ 1 gets at least 3 colours. -/
theorem every_4AP_three_colours :
    ∀ a, a < 77 → ∀ d, d < 26 → 0 < d → a + 3 * d < 77 →
      3 ≤ ndistinct (col a) (col (a + d)) (col (a + 2 * d)) (col (a + 3 * d)) := by decide
