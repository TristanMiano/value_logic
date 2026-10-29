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



set_option autoImplicit false

namespace V19

universe u v w z

variable {A : Type u} {I : Type v} {J : Type w} {B : Type z}

theorem witness_assignment (universal : Prop) (p : J → I → Prop) :
    (universal ∧ ∀ j, ∃ i, p j i) ↔
      ∃ assignment : J → I, universal ∧ ∀ j, p j (assignment j) := by
  constructor
  · intro h
    exact ⟨fun j => Classical.choose (h.2 j), h.1,
      fun j => Classical.choose_spec (h.2 j)⟩
  · intro h
    obtain ⟨assignment, hu, hp⟩ := h
    exact ⟨hu, fun j => ⟨assignment j, hp j⟩⟩

def Interval (le : A → A → Prop) (lo hi q : A) : Prop :=
  le lo q ∧ le q hi

def AttainedMinimum (le : A → A → Prop) (x : I → A) (q : A) : Prop :=
  (∃ i, x i = q) ∧ ∀ i, le q (x i)

def BranchImage (le : A → A → Prop) (lo hi : I → A) (q : A) : Prop :=
  ∃ x : I → A, (∀ i, Interval le (lo i) (hi i) (x i)) ∧
    AttainedMinimum le x q

theorem branch_projection (le : A → A → Prop)
    (refl : ∀ a, le a a)
    (trans : ∀ a b c, le a b → le b c → le a c)
    (lo hi : I → A) (nonempty : ∀ i, le (lo i) (hi i)) (q : A) :
    BranchImage le lo hi q ↔
      (∃ i, le (lo i) q) ∧ ∀ j, le q (hi j) := by
  classical
  constructor
  · intro h
    obtain ⟨x, hx, ⟨i, heq⟩, hmin⟩ := h
    refine ⟨⟨i, ?_⟩, ?_⟩
    · simpa only [heq] using (hx i).1
    · intro j
      exact trans q (x j) (hi j) (hmin j) (hx j).2
  · intro h
    obtain ⟨⟨i, hlo⟩, hhi⟩ := h
    let x : I → A := fun j => if j = i then q else hi j
    refine ⟨x, ?_, ⟨⟨i, ?_⟩, ?_⟩⟩
    · intro j
      by_cases hj : j = i
      · subst j
        simp only [x, if_pos rfl]
        exact ⟨hlo, hhi i⟩
      · simp only [x, if_neg hj]
        exact ⟨nonempty j, refl (hi j)⟩
    · simp only [x, if_pos rfl]
    · intro j
      by_cases hj : j = i
      · simp only [x, if_pos hj]
        exact refl q
      · simp only [x, if_neg hj]
        exact hhi j

def UnionImage (le : A → A → Prop) (good : B → Prop)
    (label : B → I → J) (lo hi : I → J → A) (q : A) : Prop :=
  ∃ b, good b ∧ BranchImage le (fun i => lo i (label b i))
    (fun i => hi i (label b i)) q

def AnchoredImage (le : A → A → Prop) (good : B → Prop)
    (label : B → I → J) (lo hi : I → J → A) (q : A) : Prop :=
  ∃ i t, Interval le (lo i t) (hi i t) q ∧
    ∃ b, good b ∧ label b i = t ∧
      ∀ j, j ≠ i → le q (hi j (label b j))

theorem anchor_rearrangement (le : A → A → Prop)
    (refl : ∀ a, le a a)
    (trans : ∀ a b c, le a b → le b c → le a c)
    (good : B → Prop) (label : B → I → J) (lo hi : I → J → A)
    (nonempty : ∀ b, good b → ∀ i, le (lo i (label b i)) (hi i (label b i)))
    (q : A) :
    UnionImage le good label lo hi q ↔
      AnchoredImage le good label lo hi q := by
  classical
  constructor
  · intro h
    obtain ⟨b, hb, hrange⟩ := h
    have hp := (branch_projection le refl trans
      (fun i => lo i (label b i)) (fun i => hi i (label b i))
      (nonempty b hb) q).mp hrange
    obtain ⟨⟨i, hlo⟩, hhi⟩ := hp
    exact ⟨i, label b i, ⟨hlo, hhi i⟩, b, hb, rfl,
      fun j _ => hhi j⟩
  · intro h
    obtain ⟨i, t, hlocal, b, hb, hlabel, houtside⟩ := h
    refine ⟨b, hb, ?_⟩
    apply (branch_projection le refl trans
      (fun j => lo j (label b j)) (fun j => hi j (label b j))
      (nonempty b hb) q).mpr
    refine ⟨⟨i, ?_⟩, ?_⟩
    · rw [hlabel]
      exact hlocal.1
    · intro j
      by_cases hj : j = i
      · subst j
        rw [hlabel]
        exact hlocal.2
      · exact houtside j hj

theorem attained_largest_threshold (le : A → A → Prop)
    (trans : ∀ a b c, le a b → le b c → le a c)
    (active : B → Prop) (value : B → A) (cap q : A)
    (attained : ∃ b, active b ∧ value b = cap)
    (upper : ∀ b, active b → le (value b) cap) :
    (∃ b, active b ∧ le q (value b)) ↔ le q cap := by
  constructor
  · intro h
    obtain ⟨b, hb, hq⟩ := h
    exact trans q (value b) cap hq (upper b hb)
  · intro hq
    obtain ⟨b, hb, heq⟩ := attained
    refine ⟨b, hb, ?_⟩
    rw [heq]
    exact hq

end V19

#print axioms V19.witness_assignment
#print axioms V19.branch_projection
#print axioms V19.anchor_rearrangement
#print axioms V19.attained_largest_threshold


namespace V19Source

open Std Lean.Grind V19Dual V19Local V19

universe u v
variable {R : Type u} [Field R] [LE R] [LT R]
  [LawfulOrderLT R] [IsLinearOrder R] [OrderedRing R]

def rowA (m k : Nat) (A G : Nat → Nat → R) (mask : Nat → Bool)
    (r : Nat) : Nat → R :=
  if r < m then A r else if r < m+k then (fun h => -G (r-m) h)
  else if mask (r-(m+k)) then G (r-(m+k)) else (fun _ => 0)

def rowB (m k : Nat) (base offset lower upper : Nat → R)
    (mask : Nat → Bool) (r : Nat) : R :=
  if r < m then base r else if r < m+k then offset (r-m)-lower (r-m)
  else if mask (r-(m+k)) then upper (r-(m+k))-offset (r-(m+k)) else 0

def affineCell (m d k : Nat) (A G : Nat → Nat → R)
    (base offset lower upper : Nat → R) (mask : Nat → Bool) (x : Nat → R) : Prop :=
  feasible m d A base x ∧
  (∀ j, j < k → lower j ≤ dot d (G j) x+offset j) ∧
  (∀ j, j < k → mask j=true → dot d (G j) x+offset j ≤ upper j)

theorem padded_rows_iff (m d k : Nat) (A G : Nat → Nat → R)
    (base offset lower upper : Nat → R) (mask : Nat → Bool) (x : Nat → R) :
    feasible (m+2*k) d (rowA m k A G mask)
      (rowB m k base offset lower upper mask) x ↔
    affineCell m d k A G base offset lower upper mask x := by
  constructor
  · intro h
    refine ⟨?_, ?_, ?_⟩
    · intro r hr
      have bound := h r (by omega)
      simpa [rowA, rowB, hr] using bound
    · intro j hj
      have bound := h (m+j) (by omega)
      have notbase : ¬m+j < m := by omega
      have islower : m+j < m+k := by omega
      simp only [rowA, rowB, if_neg notbase, if_pos islower,
        Nat.add_sub_cancel_left, dot_neg] at bound
      grind
    · intro j hj selected
      have bound := h (m+k+j) (by omega)
      have notbase : ¬m+k+j < m := by omega
      have notlower : ¬m+k+j < m+k := by omega
      simp [rowA, rowB, notbase, notlower, selected] at bound
      grind
  · intro h r hr
    by_cases isbase : r < m
    · simpa [rowA, rowB, isbase] using h.1 r isbase
    · by_cases islower : r < m+k
      · have bound := h.2.1 (r-m) (by omega)
        simp only [rowA, rowB, if_neg isbase, if_pos islower, dot_neg]
        grind
      · have valid : r-(m+k) < k := by omega
        by_cases selected : mask (r-(m+k))=true
        · have bound := h.2.2 (r-(m+k)) valid selected
          simp [rowA, rowB, isbase, islower, selected]
          grind
        · simp [rowA, rowB, isbase, islower, selected, dot_zero]

variable {I : Type v} {X : I → Type u}

def source (k : Nat) (base : (i : I) → X i → Prop)
    (g : Nat → (i : I) → X i → R) (lower upper : Nat → R)
    (x : (i : I) → X i) : Prop :=
  (∀ i, base i (x i)) ∧
  (∀ j, j < k → ∀ i, lower j ≤ g j i (x i)) ∧
  (∀ j, j < k → ∃ i, g j i (x i) ≤ upper j)

def cell (k : Nat) (base : (i : I) → X i → Prop)
    (g : Nat → (i : I) → X i → R) (lower upper : Nat → R)
    (i : I) (mask : Nat → Bool) (x : X i) : Prop :=
  base i x ∧ (∀ j, j < k → lower j ≤ g j i x) ∧
    (∀ j, j < k → mask j=true → g j i x ≤ upper j)

noncomputable def label (assignment : Nat → I) (i : I) : Nat → Bool := by
  classical
  exact fun j => decide (assignment j=i)

theorem source_iff_assignment (i0 : I) (k : Nat) (base : (i : I) → X i → Prop)
    (g : Nat → (i : I) → X i → R) (lower upper : Nat → R)
    (x : (i : I) → X i) :
    source k base g lower upper x ↔
      ∃ assignment : Nat → I,
        ∀ i, cell k base g lower upper i (label assignment i) (x i) := by
  classical
  constructor
  · intro h
    let assignment : Nat → I := fun j =>
      if hj : j < k then Classical.choose (h.2.2 j hj) else i0
    refine ⟨assignment, fun i => ⟨h.1 i, ?_, ?_⟩⟩
    · intro j hj
      exact h.2.1 j hj i
    · intro j hj selected
      have equal : assignment j=i := by simpa [label] using selected
      have chosenIndex : Classical.choose (h.2.2 j hj)=i := by
        simpa [assignment, hj] using equal
      have chosen := Classical.choose_spec (h.2.2 j hj)
      rw [chosenIndex] at chosen
      exact chosen
  · rintro ⟨assignment, cells⟩
    refine ⟨fun i => (cells i).1, ?_, ?_⟩
    · intro j hj i
      exact (cells i).2.1 j hj
    · intro j hj
      exact ⟨assignment j, (cells (assignment j)).2.2 j hj (by simp [label])⟩

def sourceImage (k : Nat) (base : (i : I) → X i → Prop)
    (g : Nat → (i : I) → X i → R) (lower upper : Nat → R)
    (f : (i : I) → X i → R) (q : R) : Prop :=
  ∃ x : (i : I) → X i, source k base g lower upper x ∧
    AttainedMinimum (fun a b : R => a ≤ b) (fun i => f i (x i)) q

theorem source_image_iff_union (i0 : I) (k : Nat)
    (base : (i : I) → X i → Prop)
    (g : Nat → (i : I) → X i → R) (lower upper : Nat → R)
    (f : (i : I) → X i → R) (available : I → (Nat → Bool) → Prop)
    (lo hi : I → (Nat → Bool) → R)
    (local_image : ∀ i mask q,
      (∃ x, cell k base g lower upper i mask x ∧ f i x=q) ↔
        available i mask ∧ Interval (fun a b : R => a ≤ b) (lo i mask) (hi i mask) q)
    (q : R) :
    sourceImage k base g lower upper f q ↔
      UnionImage (fun a b : R => a ≤ b)
        (fun assignment => ∀ i, available i (label assignment i)) label lo hi q := by
  classical
  constructor
  · rintro ⟨x, hx, minimum⟩
    obtain ⟨assignment, cells⟩ :=
      (source_iff_assignment i0 k base g lower upper x).mp hx
    have localFacts : ∀ i, available i (label assignment i) ∧
        Interval (fun a b : R => a ≤ b) (lo i (label assignment i))
          (hi i (label assignment i)) (f i (x i)) := by
      intro i
      exact (local_image i (label assignment i) (f i (x i))).mp ⟨x i, cells i, rfl⟩
    exact ⟨assignment, fun i => (localFacts i).1,
      (fun i => f i (x i)), (fun i => (localFacts i).2), minimum⟩
  · rintro ⟨assignment, good, values, intervals, minimum⟩
    have witnesses : ∀ i, ∃ x, cell k base g lower upper i (label assignment i) x ∧
        f i x=values i := by
      intro i
      exact (local_image i (label assignment i) (values i)).mpr ⟨good i, intervals i⟩
    let x : (i : I) → X i := fun i => Classical.choose (witnesses i)
    have facts : ∀ i, cell k base g lower upper i (label assignment i) (x i) ∧
        f i (x i)=values i := fun i => Classical.choose_spec (witnesses i)
    have equal : (fun i => f i (x i))=values := funext (fun i => (facts i).2)
    refine ⟨x, (source_iff_assignment i0 k base g lower upper x).mpr
      ⟨assignment, fun i => (facts i).1⟩, ?_⟩
    rw [equal]
    exact minimum

theorem source_image_iff_anchor (i0 : I) (k : Nat)
    (base : (i : I) → X i → Prop)
    (g : Nat → (i : I) → X i → R) (lower upper : Nat → R)
    (f : (i : I) → X i → R) (available : I → (Nat → Bool) → Prop)
    (lo hi : I → (Nat → Bool) → R)
    (nonempty : ∀ i mask, available i mask → lo i mask ≤ hi i mask)
    (local_image : ∀ i mask q,
      (∃ x, cell k base g lower upper i mask x ∧ f i x=q) ↔
        available i mask ∧ Interval (fun a b : R => a ≤ b) (lo i mask) (hi i mask) q)
    (q : R) :
    sourceImage k base g lower upper f q ↔
      AnchoredImage (fun a b : R => a ≤ b)
        (fun assignment => ∀ i, available i (label assignment i)) label lo hi q := by
  apply (source_image_iff_union i0 k base g lower upper f available lo hi local_image q).trans
  exact anchor_rearrangement (fun a b : R => a ≤ b) (fun _ => Std.le_refl _)
    (fun _ _ _ h1 h2 => Std.le_trans h1 h2)
    (fun assignment => ∀ i, available i (label assignment i)) label lo hi
    (fun assignment good i => nonempty i (label assignment i) (good i)) q

#print axioms padded_rows_iff
#print axioms source_iff_assignment
#print axioms source_image_iff_union
#print axioms source_image_iff_anchor

end V19Source


namespace V19Certified

open Std Lean.Grind V19Dual V19Local V19Source V19

universe u v
variable {R : Type u} [Field R] [LE R] [LT R]
  [LawfulOrderLT R] [IsLinearOrder R] [OrderedRing R]

structure Bounds (m d : Nat) (A : Nat → Nat → R)
    (b c : Nat → R) (offset : R) where
  lo : R
  hi : R
  lowPoint : Nat → R
  highPoint : Nat → R
  lowDual : Nat → R
  highDual : Nat → R
  lowNonnegative : ∀ r, r < m → 0 ≤ lowDual r
  highNonnegative : ∀ r, r < m → 0 ≤ highDual r
  lowColumns : ∀ j, j < d → total m (fun r => lowDual r*A r j) = -c j
  highColumns : ∀ j, j < d → total m (fun r => highDual r*A r j) = c j
  lowFeasible : feasible m d A b lowPoint
  highFeasible : feasible m d A b highPoint
  lowValue : dot d c lowPoint+offset=lo
  highValue : dot d c highPoint+offset=hi
  lowBound : offset-total m (fun r => lowDual r*b r)=lo
  highBound : offset+total m (fun r => highDual r*b r)=hi

inductive Certificate (m d : Nat) (A : Nat → Nat → R)
    (b c : Nat → R) (offset : R) where
  | empty (dual : Nat → R)
      (nonnegative : ∀ r, r < m → 0 ≤ dual r)
      (columns : ∀ j, j < d → total m (fun r => dual r*A r j)=0)
      (negative : total m (fun r => dual r*b r)<0)
  | bounded (data : Bounds m d A b c offset)

namespace Certificate

variable {m d : Nat} {A : Nat → Nat → R} {b c : Nat → R} {offset : R}

def available : Certificate m d A b c offset → Prop
  | .empty .. => False
  | .bounded _ => True

def lo : Certificate m d A b c offset → R
  | .empty .. => 0
  | .bounded data => data.lo

def hi : Certificate m d A b c offset → R
  | .empty .. => 0
  | .bounded data => data.hi

theorem image (cert : Certificate m d A b c offset) (q : R) :
    (∃ x, feasible m d A b x ∧ dot d c x+offset=q) ↔
      cert.available ∧ Interval (fun a b : R => a ≤ b) cert.lo cert.hi q := by
  cases cert with
  | empty dual nonnegative columns negative =>
    constructor
    · rintro ⟨x, hx, _⟩
      exact False.elim ((farkas_exclusion m d A b dual nonnegative columns negative) ⟨x, hx⟩)
    · rintro ⟨impossible, _⟩
      exact False.elim impossible
  | bounded data =>
    have equal := certified_interval_image m d A b c data.lowPoint data.highPoint
      data.lowDual data.highDual offset data.lo data.hi q
      data.lowNonnegative data.highNonnegative data.lowColumns data.highColumns
      data.lowFeasible data.highFeasible data.lowValue data.highValue
      data.lowBound data.highBound
    change (∃ x, feasible m d A b x ∧ dot d c x+offset=q) ↔
      True ∧ (data.lo ≤ q ∧ q ≤ data.hi)
    exact equal.trans (by simp)

theorem ordered (cert : Certificate m d A b c offset) :
    cert.available → cert.lo ≤ cert.hi := by
  cases cert with
  | empty dual nonnegative columns negative =>
    intro impossible
    exact False.elim impossible
  | bounded data =>
    intro _
    have inside := (image (.bounded data) data.lo).mp
      ⟨data.lowPoint, data.lowFeasible, data.lowValue⟩
    exact inside.2.2

end Certificate

abbrev ReceiptCertificate (m d k : Nat) (A G : Nat → Nat → R)
    (base offset lower upper : Nat → R) (mask : Nat → Bool)
    (c : Nat → R) (futureOffset : R) :=
  Certificate (m+2*k) d (rowA m k A G mask)
    (rowB m k base offset lower upper mask) c futureOffset

theorem receipt_certificate_image (m d k : Nat) (A G : Nat → Nat → R)
    (base offset lower upper : Nat → R) (mask : Nat → Bool)
    (c : Nat → R) (futureOffset : R)
    (cert : ReceiptCertificate m d k A G base offset lower upper mask c futureOffset)
    (q : R) :
    (∃ x, affineCell m d k A G base offset lower upper mask x ∧
      dot d c x+futureOffset=q) ↔
      cert.available ∧ Interval (fun a b : R => a ≤ b) cert.lo cert.hi q := by
  have equal := cert.image q
  constructor
  · rintro ⟨x, hx, value⟩
    exact equal.mp ⟨x, (padded_rows_iff m d k A G base offset lower upper mask x).mpr hx, value⟩
  · intro accepted
    obtain ⟨x, hx, value⟩ := equal.mpr accepted
    exact ⟨x, (padded_rows_iff m d k A G base offset lower upper mask x).mp hx, value⟩

variable {I : Type v}

theorem complete_certificate_source_image (i0 : I) (k : Nat)
    (m d : I → Nat) (A G : I → Nat → Nat → R)
    (base offset : I → Nat → R) (lower upper : Nat → R)
    (c : I → Nat → R) (futureOffset : I → R)
    (certs : ∀ i mask, ReceiptCertificate (m i) (d i) k (A i) (G i)
      (base i) (offset i) lower upper mask (c i) (futureOffset i))
    (q : R) :
    sourceImage k (fun i x => feasible (m i) (d i) (A i) (base i) x)
      (fun j i x => dot (d i) (G i j) x+offset i j) lower upper
      (fun i x => dot (d i) (c i) x+futureOffset i) q ↔
    AnchoredImage (fun a b : R => a ≤ b)
      (fun assignment => ∀ i, (certs i (label assignment i)).available) label
      (fun i mask => (certs i mask).lo) (fun i mask => (certs i mask).hi) q := by
  apply source_image_iff_anchor i0 k
    (fun i x => feasible (m i) (d i) (A i) (base i) x)
    (fun j i x => dot (d i) (G i j) x+offset i j) lower upper
    (fun i x => dot (d i) (c i) x+futureOffset i)
    (fun i mask => (certs i mask).available)
    (fun i mask => (certs i mask).lo) (fun i mask => (certs i mask).hi)
    (fun i mask => (certs i mask).ordered)
  intro i mask value
  exact receipt_certificate_image (m i) (d i) k (A i) (G i)
    (base i) (offset i) lower upper mask (c i) (futureOffset i) (certs i mask) value

#print axioms Certificate.image
#print axioms Certificate.ordered
#print axioms receipt_certificate_image
#print axioms complete_certificate_source_image

end V19Certified


namespace V19Finite

open Std Lean.Grind V19Dual V19Local V19Source V19Certified V19

universe u v
variable {R : Type u} [Field R] [LE R] [LT R]
  [LawfulOrderLT R] [IsLinearOrder R] [OrderedRing R]
variable {I : Type v} {k : Nat}

def extendMask (mask : Fin k → Bool) (j : Nat) : Bool :=
  if hj : j < k then mask ⟨j,hj⟩ else false

noncomputable def finiteLabel (assignment : Fin k → I) (i : I) : Fin k → Bool := by
  classical
  exact fun j => decide (assignment j=i)

theorem source_iff_finite_assignment {X : I → Type u}
    (base : (i : I) → X i → Prop)
    (g : Nat → (i : I) → X i → R) (lower upper : Nat → R)
    (x : (i : I) → X i) :
    source k base g lower upper x ↔
      ∃ assignment : Fin k → I,
        ∀ i, cell k base g lower upper i (extendMask (finiteLabel assignment i)) (x i) := by
  classical
  constructor
  · intro h
    let assignment : Fin k → I := fun j => Classical.choose (h.2.2 j.val j.isLt)
    refine ⟨assignment, fun i => ⟨h.1 i, ?_, ?_⟩⟩
    · intro j hj
      exact h.2.1 j hj i
    · intro j hj selected
      have equal : assignment ⟨j,hj⟩=i := by
        simpa [extendMask, finiteLabel, hj] using selected
      have chosen : g j (assignment ⟨j,hj⟩) (x (assignment ⟨j,hj⟩)) ≤ upper j :=
        Classical.choose_spec (h.2.2 j hj)
      rw [equal] at chosen
      exact chosen
  · rintro ⟨assignment, cells⟩
    refine ⟨fun i => (cells i).1, ?_, ?_⟩
    · intro j hj i
      exact (cells i).2.1 j hj
    · intro j hj
      exact ⟨assignment ⟨j,hj⟩, (cells (assignment ⟨j,hj⟩)).2.2 j hj
        (by simp [extendMask, finiteLabel, hj])⟩

theorem finite_source_image_iff_union {X : I → Type u}
    (base : (i : I) → X i → Prop)
    (g : Nat → (i : I) → X i → R) (lower upper : Nat → R)
    (f : (i : I) → X i → R) (available : I → (Fin k → Bool) → Prop)
    (lo hi : I → (Fin k → Bool) → R)
    (local_image : ∀ i mask q,
      (∃ x, cell k base g lower upper i (extendMask mask) x ∧ f i x=q) ↔
        available i mask ∧ Interval (fun a b : R => a ≤ b) (lo i mask) (hi i mask) q)
    (q : R) :
    sourceImage k base g lower upper f q ↔
      UnionImage (fun a b : R => a ≤ b)
        (fun assignment => ∀ i, available i (finiteLabel assignment i)) finiteLabel lo hi q := by
  classical
  constructor
  · rintro ⟨x, hx, minimum⟩
    obtain ⟨assignment, cells⟩ := (source_iff_finite_assignment base g lower upper x).mp hx
    have localFacts : ∀ i, available i (finiteLabel assignment i) ∧
        Interval (fun a b : R => a ≤ b) (lo i (finiteLabel assignment i))
          (hi i (finiteLabel assignment i)) (f i (x i)) := by
      intro i
      exact (local_image i (finiteLabel assignment i) (f i (x i))).mp ⟨x i, cells i, rfl⟩
    exact ⟨assignment, fun i => (localFacts i).1,
      (fun i => f i (x i)), (fun i => (localFacts i).2), minimum⟩
  · rintro ⟨assignment, good, values, intervals, minimum⟩
    have witnesses : ∀ i, ∃ x,
        cell k base g lower upper i (extendMask (finiteLabel assignment i)) x ∧
        f i x=values i := by
      intro i
      exact (local_image i (finiteLabel assignment i) (values i)).mpr ⟨good i, intervals i⟩
    let x : (i : I) → X i := fun i => Classical.choose (witnesses i)
    have facts : ∀ i,
        cell k base g lower upper i (extendMask (finiteLabel assignment i)) (x i) ∧
        f i (x i)=values i := fun i => Classical.choose_spec (witnesses i)
    have equal : (fun i => f i (x i))=values := funext (fun i => (facts i).2)
    refine ⟨x, (source_iff_finite_assignment base g lower upper x).mpr
      ⟨assignment, fun i => (facts i).1⟩, ?_⟩
    rw [equal]
    exact minimum

theorem finite_complete_certificate_image
    (m d : I → Nat) (A G : I → Nat → Nat → R)
    (base offset : I → Nat → R) (lower upper : Nat → R)
    (c : I → Nat → R) (futureOffset : I → R)
    (certs : ∀ i (mask : Fin k → Bool), ReceiptCertificate (m i) (d i) k (A i) (G i)
      (base i) (offset i) lower upper (extendMask mask) (c i) (futureOffset i))
    (q : R) :
    sourceImage k (fun i x => feasible (m i) (d i) (A i) (base i) x)
      (fun j i x => dot (d i) (G i j) x+offset i j) lower upper
      (fun i x => dot (d i) (c i) x+futureOffset i) q ↔
    AnchoredImage (fun a b : R => a ≤ b)
      (fun assignment => ∀ i, (certs i (finiteLabel assignment i)).available) finiteLabel
      (fun i mask => (certs i mask).lo) (fun i mask => (certs i mask).hi) q := by
  have locals : ∀ i mask value,
      (∃ x, cell k (fun i x => feasible (m i) (d i) (A i) (base i) x)
        (fun j i x => dot (d i) (G i j) x+offset i j) lower upper i (extendMask mask) x ∧
        dot (d i) (c i) x+futureOffset i=value) ↔
      (certs i mask).available ∧
        Interval (fun a b : R => a ≤ b) (certs i mask).lo (certs i mask).hi value := by
    intro i mask value
    exact receipt_certificate_image (m i) (d i) k (A i) (G i)
      (base i) (offset i) lower upper (extendMask mask) (c i) (futureOffset i) (certs i mask) value
  apply (finite_source_image_iff_union
    (fun i x => feasible (m i) (d i) (A i) (base i) x)
    (fun j i x => dot (d i) (G i j) x+offset i j) lower upper
    (fun i x => dot (d i) (c i) x+futureOffset i)
    (fun i mask => (certs i mask).available)
    (fun i mask => (certs i mask).lo) (fun i mask => (certs i mask).hi) locals q).trans
  exact anchor_rearrangement (fun a b : R => a ≤ b) (fun _ => Std.le_refl _)
    (fun _ _ _ h1 h2 => Std.le_trans h1 h2)
    (fun assignment => ∀ i, (certs i (finiteLabel assignment i)).available)
    finiteLabel (fun i mask => (certs i mask).lo) (fun i mask => (certs i mask).hi)
    (fun assignment good i => (certs i (finiteLabel assignment i)).ordered (good i)) q

#print axioms source_iff_finite_assignment
#print axioms finite_source_image_iff_union
#print axioms finite_complete_certificate_image

end V19Finite
