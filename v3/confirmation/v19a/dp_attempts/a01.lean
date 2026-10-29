import Std

set_option autoImplicit false

namespace V19DP

universe u v w z
variable {S : Type u} {E : Type v} {G : Type w} {W : Type z}

def best (le : S → S → Prop) [DecidableRel le] (score : E → S) :
    List E → Option E
  | [] => none
  | e :: es => match best le score es with
    | none => some e
    | some b => some (if le (score e) (score b) then b else e)

theorem best_none_iff (le : S → S → Prop) [DecidableRel le]
    (score : E → S) (es : List E) : best le score es = none ↔ es = [] := by
  cases es with
  | nil => simp [best]
  | cons e es =>
    cases h : best le score es <;> simp [best, h]

theorem best_spec (le : S → S → Prop) [DecidableRel le]
    (refl : ∀ a, le a a)
    (trans : ∀ a b c, le a b → le b c → le a c)
    (total : ∀ a b, le a b ∨ le b a)
    (score : E → S) (es : List E) (b : E)
    (answer : best le score es = some b) :
    b ∈ es ∧ ∀ e, e ∈ es → le (score e) (score b) := by
  induction es generalizing b with
  | nil => simp [best] at answer
  | cons e es ih =>
    cases h : best le score es with
    | none =>
      have empty : es = [] := (best_none_iff le score es).mp h
      subst es
      have same : e = b := by simpa [best] using answer
      subst b
      constructor
      · simp
      · intro x hx
        have same : x = e := by simpa using hx
        subst x
        exact refl (score e)
    | some c =>
      have hc := ih c h
      by_cases order : le (score e) (score c)
      · have same : c = b := by simpa [best, h, order] using answer
        subst b
        constructor
        · exact List.mem_cons_of_mem e hc.1
        · intro x hx
          rcases List.mem_cons.mp hx with hx | hx
          · subst x
            exact order
          · exact hc.2 x hx
      · have same : e = b := by simpa [best, h, order] using answer
        subst b
        have reverse : le (score c) (score e) :=
          (total (score e) (score c)).resolve_left order
        constructor
        · simp
        · intro x hx
          rcases List.mem_cons.mp hx with hx | hx
          · subst x
            exact refl (score e)
          · exact trans (score x) (score c) (score e) (hc.2 x hx) reverse

def expanded (groups : List G) (children : G → List W) : List (G × W) :=
  groups.flatMap (fun g => (children g).map (fun w => (g,w)))

def compressed (le : S → S → Prop) [DecidableRel le] (score : W → S)
    (groups : List G) (children : G → List W) : List (G × W) :=
  groups.flatMap (fun g => (best le score (children g)).toList.map (fun w => (g,w)))

theorem mem_expanded (groups : List G) (children : G → List W) (g : G) (w : W) :
    (g,w) ∈ expanded groups children ↔ g ∈ groups ∧ w ∈ children g := by
  simp [expanded, List.mem_flatMap, List.mem_map]

theorem mem_compressed (le : S → S → Prop) [DecidableRel le] (score : W → S)
    (groups : List G) (children : G → List W) (g : G) (w : W) :
    (g,w) ∈ compressed le score groups children ↔
      g ∈ groups ∧ best le score (children g) = some w := by
  simp [compressed, List.mem_flatMap, List.mem_map]

theorem compression_preserves_argmax (le : S → S → Prop) [DecidableRel le]
    (refl : ∀ a, le a a)
    (trans : ∀ a b c, le a b → le b c → le a c)
    (total : ∀ a b, le a b ∨ le b a)
    (score : W → S) (parent : G × W → S)
    (monotone : ∀ g a b, le (score a) (score b) →
      le (parent (g,a)) (parent (g,b)))
    (groups : List G) (children : G → List W) (winner : G × W)
    (answer : best le parent (compressed le score groups children) = some winner) :
    winner ∈ expanded groups children ∧
      ∀ candidate, candidate ∈ expanded groups children →
        le (parent candidate) (parent winner) := by
  have outer := best_spec le refl trans total parent
    (compressed le score groups children) winner answer
  rcases winner with ⟨g,w⟩
  have hw := (mem_compressed le score groups children g w).mp outer.1
  have hLocal := best_spec le refl trans total score (children g) w hw.2
  constructor
  · exact (mem_expanded groups children g w).mpr ⟨hw.1, hLocal.1⟩
  · intro candidate hc
    rcases candidate with ⟨j,x⟩
    have hx := (mem_expanded groups children j x).mp hc
    cases h : best le score (children j) with
    | none =>
      have empty := (best_none_iff le score (children j)).mp h
      simp [empty] at hx
    | some y =>
      have hy := best_spec le refl trans total score (children j) y h
      have representative : (j,y) ∈ compressed le score groups children :=
        (mem_compressed le score groups children j y).mpr ⟨hx.1,h⟩
      exact trans (parent (j,x)) (parent (j,y)) (parent (g,w))
        (monotone j x y (hy.2 x hx.2)) (outer.2 (j,y) representative)

theorem compressed_empty_iff (le : S → S → Prop) [DecidableRel le]
    (refl : ∀ a, le a a)
    (trans : ∀ a b c, le a b → le b c → le a c)
    (total : ∀ a b, le a b ∨ le b a)
    (score : W → S) (groups : List G) (children : G → List W) :
    compressed le score groups children = [] ↔ expanded groups children = [] := by
  constructor
  · intro empty
    apply List.eq_nil_iff_forall_not_mem.mpr
    intro candidate hc
    rcases candidate with ⟨g,w⟩
    have hw := (mem_expanded groups children g w).mp hc
    cases h : best le score (children g) with
    | none =>
      have noChildren := (best_none_iff le score (children g)).mp h
      simp [noChildren] at hw
    | some y =>
      have member := (mem_compressed le score groups children g y).mpr ⟨hw.1,h⟩
      simp [empty] at member
  · intro empty
    apply List.eq_nil_iff_forall_not_mem.mpr
    intro candidate hc
    rcases candidate with ⟨g,w⟩
    have hw := (mem_compressed le score groups children g w).mp hc
    have hLocal := best_spec le refl trans total score (children g) w hw.2
    have member := (mem_expanded groups children g w).mpr ⟨hw.1,hLocal.1⟩
    simp [empty] at member

theorem meet_monotone_right (le : S → S → Prop)
    (trans : ∀ a b c, le a b → le b c → le a c)
    (meet : S → S → S)
    (left : ∀ a b, le (meet a b) a)
    (right : ∀ a b, le (meet a b) b)
    (greatest : ∀ a b c, le c a → le c b → le c (meet a b))
    (a b c : S) (order : le b c) : le (meet a b) (meet a c) := by
  exact greatest a c (meet a b) (left a b)
    (trans (meet a b) b c (right a b) order)

end V19DP

#print axioms V19DP.best_none_iff
#print axioms V19DP.best_spec
#print axioms V19DP.compression_preserves_argmax
#print axioms V19DP.compressed_empty_iff
#print axioms V19DP.meet_monotone_right
