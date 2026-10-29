import Std
import Init.Grind.Ordered.Field

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

namespace V19Local

open Std Lean.Grind V19Dual

universe u
variable {R : Type u} [Field R] [LE R] [LT R]
  [LawfulOrderLT R] [IsLinearOrder R] [OrderedRing R]

def mix (t : R) (x y : Nat → R) : Nat → R :=
  fun j => (1-t)*x j + t*y j

theorem dot_mix (d : Nat) (c x y : Nat → R) (t : R) :
    dot d c (mix t x y) = (1-t)*dot d c x + t*dot d c y := by
  induction d with
  | zero => simp [dot]; grind
  | succ d ih => simp [dot, ih, mix]; grind

theorem affine_mix (d : Nat) (c x y : Nat → R) (t offset : R) :
    dot d c (mix t x y) + offset =
      (1-t)*(dot d c x + offset) + t*(dot d c y + offset) := by
  rw [dot_mix]
  grind

theorem feasible_mix (m d : Nat) (A : Nat → Nat → R) (b x y : Nat → R)
    (t : R) (t_nonnegative : 0 ≤ t) (t_at_most_one : t ≤ 1)
    (hx : feasible m d A b x) (hy : feasible m d A b y) :
    feasible m d A b (mix t x y) := by
  intro i hi
  have left_nonnegative : 0 ≤ 1-t := by grind
  have left := OrderedRing.mul_le_mul_of_nonneg_left (hx i hi) left_nonnegative
  have right := OrderedRing.mul_le_mul_of_nonneg_left (hy i hi) t_nonnegative
  rw [dot_mix]
  grind

theorem interpolation_coefficient (lo hi q : R) (hlo : lo ≤ q)
    (hhi : q ≤ hi) (strict : lo < hi) :
    let t := (q-lo)*(hi-lo)⁻¹
    0 ≤ t ∧ t ≤ 1 ∧ (1-t)*lo+t*hi=q := by
  have gap_positive : 0 < hi-lo := by grind
  have gap_nonzero : hi-lo ≠ 0 := by grind
  have numerator_nonnegative : 0 ≤ q-lo := by grind
  have inv_nonnegative : 0 ≤ (hi-lo)⁻¹ :=
    Field.IsOrdered.inv_nonneg_iff.mpr (by grind)
  have numerator_bound : q-lo ≤ hi-lo := by grind
  have lower := OrderedRing.mul_nonneg numerator_nonnegative inv_nonnegative
  have upper := OrderedRing.mul_le_mul_of_nonneg_right numerator_bound inv_nonnegative
  have inverse := Field.mul_inv_cancel (a := hi-lo) gap_nonzero
  rw [inverse] at upper
  have product_identity : ((q-lo)*(hi-lo)⁻¹)*(hi-lo)=q-lo := by
    rw [Semiring.mul_assoc, Field.inv_mul_cancel gap_nonzero, Semiring.mul_one]
  dsimp
  exact ⟨lower, upper, by grind⟩

theorem local_interval_image (m d : Nat) (A : Nat → Nat → R)
    (b c low_point high_point : Nat → R) (offset lo hi q : R)
    (low_feasible : feasible m d A b low_point)
    (high_feasible : feasible m d A b high_point)
    (low_value : dot d c low_point+offset=lo)
    (high_value : dot d c high_point+offset=hi)
    (lower : ∀ x, feasible m d A b x → lo ≤ dot d c x+offset)
    (upper : ∀ x, feasible m d A b x → dot d c x+offset ≤ hi) :
    (∃ x, feasible m d A b x ∧ dot d c x+offset=q) ↔ lo ≤ q ∧ q ≤ hi := by
  constructor
  · rintro ⟨x, hx, value⟩
    have hl := lower x hx
    have hu := upper x hx
    rw [value] at hl hu
    exact ⟨hl, hu⟩
  · rintro ⟨hqlo, hqhi⟩
    by_cases equal : lo=hi
    · have hq : lo=q := by grind
      exact ⟨low_point, low_feasible, low_value.trans hq⟩
    · have strict : lo < hi := by grind
      let t := (q-lo)*(hi-lo)⁻¹
      have facts := interpolation_coefficient lo hi q hqlo hqhi strict
      change 0 ≤ t ∧ t ≤ 1 ∧ (1-t)*lo+t*hi=q at facts
      refine ⟨mix t low_point high_point,
        feasible_mix m d A b low_point high_point t facts.1 facts.2.1
          low_feasible high_feasible, ?_⟩
      rw [affine_mix, low_value, high_value]
      exact facts.2.2

theorem certified_interval_image (m d : Nat) (A : Nat → Nat → R)
    (b c low_point high_point low_dual high_dual : Nat → R)
    (offset lo hi q : R)
    (low_nonnegative : ∀ i, i < m → 0 ≤ low_dual i)
    (high_nonnegative : ∀ i, i < m → 0 ≤ high_dual i)
    (low_columns : ∀ j, j < d → total m (fun i => low_dual i*A i j) = -c j)
    (high_columns : ∀ j, j < d → total m (fun i => high_dual i*A i j) = c j)
    (low_feasible : feasible m d A b low_point)
    (high_feasible : feasible m d A b high_point)
    (low_value : dot d c low_point+offset=lo)
    (high_value : dot d c high_point+offset=hi)
    (low_bound : offset-total m (fun i => low_dual i*b i)=lo)
    (high_bound : offset+total m (fun i => high_dual i*b i)=hi) :
    (∃ x, feasible m d A b x ∧ dot d c x+offset=q) ↔ lo ≤ q ∧ q ≤ hi := by
  have lower := attained_lower m d A b c low_dual low_point offset lo
    low_nonnegative low_columns low_feasible low_value low_bound
  have upper := attained_upper m d A b c high_dual high_point offset hi
    high_nonnegative high_columns high_feasible high_value high_bound
  exact local_interval_image m d A b c low_point high_point offset lo hi q
    low_feasible high_feasible low_value high_value lower.2 upper.2

#print axioms dot_mix
#print axioms feasible_mix
#print axioms interpolation_coefficient
#print axioms local_interval_image
#print axioms certified_interval_image

end V19Local
