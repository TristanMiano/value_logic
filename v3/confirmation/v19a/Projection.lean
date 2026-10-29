import Std

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
