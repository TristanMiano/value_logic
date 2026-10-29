import Std
import Init.Grind.Ordered.Ring

set_option autoImplicit false

namespace V19Dual

open Std Lean.Grind

universe u
variable {R : Type u} [CommRing R] [LE R] [LT R]
  [LawfulOrderLT R] [IsLinearOrder R] [OrderedRing R]

def total : Nat → (Nat → R) → R
  | 0, _ => 0
  | n+1, f => total n f + f n

def dot : Nat → (Nat → R) → (Nat → R) → R
  | 0, _, _ => 0
  | n+1, a, x => dot n a x + a n * x n

theorem total_zero (n : Nat) : total n (fun _ => (0 : R)) = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [total, ih]; grind

theorem total_congr (n : Nat) (f g : Nat → R)
    (h : ∀ j, j < n → f j = g j) : total n f = total n g := by
  induction n with
  | zero => rfl
  | succ n ih =>
    have old : ∀ j, j < n → f j = g j := by
      intro j hj
      exact h j (by omega)
    have last := h n (by omega)
    simp [total, ih old, last]

theorem dot_zero (n : Nat) (x : Nat → R) : dot n (fun _ => 0) x = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [dot, ih]; grind

theorem dot_congr (n : Nat) (a b x : Nat → R)
    (h : ∀ j, j < n → a j = b j) : dot n a x = dot n b x := by
  induction n with
  | zero => rfl
  | succ n ih =>
    have old : ∀ j, j < n → a j = b j := by
      intro j hj
      exact h j (by omega)
    have last := h n (by omega)
    simp [dot, ih old, last]

theorem dot_add (n : Nat) (a b x : Nat → R) :
    dot n (fun j => a j + b j) x = dot n a x + dot n b x := by
  induction n with
  | zero => simp [dot]; grind
  | succ n ih => simp [dot, ih]; grind

theorem dot_scale (n : Nat) (s : R) (a x : Nat → R) :
    dot n (fun j => s * a j) x = s * dot n a x := by
  induction n with
  | zero => simp [dot]; grind
  | succ n ih => simp [dot, ih]; grind

theorem dot_neg (n : Nat) (a x : Nat → R) :
    dot n (fun j => -a j) x = -dot n a x := by
  induction n with
  | zero => simp [dot]; grind
  | succ n ih => simp [dot, ih]; grind

theorem weighted_rows (m d : Nat) (A : Nat → Nat → R) (y x : Nat → R) :
    dot d (fun j => total m (fun i => y i * A i j)) x =
      total m (fun i => y i * dot d (A i) x) := by
  induction m with
  | zero => simp [total, dot_zero]
  | succ m ih =>
    change dot d (fun j => total m (fun i => y i * A i j) + y m * A m j) x =
      total m (fun i => y i * dot d (A i) x) + y m * dot d (A m) x
    rw [dot_add, ih, dot_scale]

theorem total_le (n : Nat) (f g : Nat → R)
    (h : ∀ j, j < n → f j ≤ g j) : total n f ≤ total n g := by
  induction n with
  | zero => simp [total]
  | succ n ih =>
    have old : ∀ j, j < n → f j ≤ g j := by
      intro j hj
      exact h j (by omega)
    have hold := ih old
    have last := h n (by omega)
    simp only [total]
    grind

def feasible (m d : Nat) (A : Nat → Nat → R) (b x : Nat → R) : Prop :=
  ∀ i, i < m → dot d (A i) x ≤ b i

theorem weak_dual (m d : Nat) (A : Nat → Nat → R) (b c y x : Nat → R)
    (nonnegative : ∀ i, i < m → 0 ≤ y i)
    (columns : ∀ j, j < d → total m (fun i => y i * A i j) = c j)
    (primal : feasible m d A b x) :
    dot d c x ≤ total m (fun i => y i * b i) := by
  have weighted : total m (fun i => y i * dot d (A i) x) ≤
      total m (fun i => y i * b i) := by
    apply total_le
    intro i hi
    exact OrderedRing.mul_le_mul_of_nonneg_left (primal i hi) (nonnegative i hi)
  have equal := dot_congr d (fun j => total m (fun i => y i * A i j)) c x columns
  rw [weighted_rows] at equal
  rw [← equal]
  exact weighted

theorem lower_dual (m d : Nat) (A : Nat → Nat → R) (b c y x : Nat → R)
    (offset : R) (nonnegative : ∀ i, i < m → 0 ≤ y i)
    (columns : ∀ j, j < d → total m (fun i => y i * A i j) = -c j)
    (primal : feasible m d A b x) :
    offset - total m (fun i => y i * b i) ≤ dot d c x + offset := by
  have bound := weak_dual m d A b (fun j => -c j) y x nonnegative columns primal
  rw [dot_neg] at bound
  grind

theorem upper_dual (m d : Nat) (A : Nat → Nat → R) (b c y x : Nat → R)
    (offset : R) (nonnegative : ∀ i, i < m → 0 ≤ y i)
    (columns : ∀ j, j < d → total m (fun i => y i * A i j) = c j)
    (primal : feasible m d A b x) :
    dot d c x + offset ≤ offset + total m (fun i => y i * b i) := by
  have bound := weak_dual m d A b c y x nonnegative columns primal
  grind

theorem farkas_exclusion (m d : Nat) (A : Nat → Nat → R) (b y : Nat → R)
    (nonnegative : ∀ i, i < m → 0 ≤ y i)
    (columns : ∀ j, j < d → total m (fun i => y i * A i j) = 0)
    (negative : total m (fun i => y i * b i) < 0) :
    ¬ ∃ x, feasible m d A b x := by
  rintro ⟨x, primal⟩
  have bound := weak_dual m d A b (fun _ => 0) y x nonnegative columns primal
  rw [dot_zero] at bound
  grind

theorem attained_lower (m d : Nat) (A : Nat → Nat → R) (b c y point : Nat → R)
    (offset value : R) (nonnegative : ∀ i, i < m → 0 ≤ y i)
    (columns : ∀ j, j < d → total m (fun i => y i * A i j) = -c j)
    (point_feasible : feasible m d A b point)
    (point_value : dot d c point + offset = value)
    (matching_bound : offset - total m (fun i => y i * b i) = value) :
    (∃ x, feasible m d A b x ∧ dot d c x + offset = value) ∧
      ∀ x, feasible m d A b x → value ≤ dot d c x + offset := by
  constructor
  · exact ⟨point, point_feasible, point_value⟩
  · intro x hx
    have bound := lower_dual m d A b c y x offset nonnegative columns hx
    rw [matching_bound] at bound
    exact bound

theorem attained_upper (m d : Nat) (A : Nat → Nat → R) (b c y point : Nat → R)
    (offset value : R) (nonnegative : ∀ i, i < m → 0 ≤ y i)
    (columns : ∀ j, j < d → total m (fun i => y i * A i j) = c j)
    (point_feasible : feasible m d A b point)
    (point_value : dot d c point + offset = value)
    (matching_bound : offset + total m (fun i => y i * b i) = value) :
    (∃ x, feasible m d A b x ∧ dot d c x + offset = value) ∧
      ∀ x, feasible m d A b x → dot d c x + offset ≤ value := by
  constructor
  · exact ⟨point, point_feasible, point_value⟩
  · intro x hx
    have bound := upper_dual m d A b c y x offset nonnegative columns hx
    rw [matching_bound] at bound
    exact bound

#print axioms weak_dual
#print axioms lower_dual
#print axioms upper_dual
#print axioms farkas_exclusion
#print axioms attained_lower
#print axioms attained_upper

end V19Dual
