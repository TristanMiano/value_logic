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

namespace V19Layer

universe u v w
variable {S : Type u} {G : Type v} {Q : Type w}

def Correct (le : S → S → Prop) (cost : G → S)
    (answer : Option G) (all : List G) : Prop :=
  (answer=none ↔ all=[]) ∧
    ∀ winner, answer=some winner →
      winner ∈ all ∧ ∀ candidate, candidate ∈ all → le (cost candidate) (cost winner)

theorem best_of_cover (le : S → S → Prop) [DecidableRel le]
    (refl : ∀ a, le a a)
    (trans : ∀ a b c, le a b → le b c → le a c)
    (total : ∀ a b, le a b ∨ le b a)
    (cost : G → S) (thin wide : List G)
    (sound : ∀ p, p ∈ thin → p ∈ wide)
    (cover : ∀ p, p ∈ wide → ∃ q, q ∈ thin ∧ le (cost p) (cost q)) :
    Correct le cost (V19DP.best le cost thin) wide := by
  constructor
  · rw [V19DP.best_none_iff]
    constructor
    · intro empty
      apply List.eq_nil_iff_forall_not_mem.mpr
      intro p hp
      obtain ⟨q,hq,_⟩ := cover p hp
      simp [empty] at hq
    · intro empty
      apply List.eq_nil_iff_forall_not_mem.mpr
      intro p hp
      have hw := sound p hp
      simp [empty] at hw
  · intro winner answer
    have hw := V19DP.best_spec le refl trans total cost thin winner answer
    constructor
    · exact sound winner hw.1
    · intro p hp
      obtain ⟨q,hq,hpq⟩ := cover p hp
      exact trans (cost p) (cost q) (cost winner) hpq (hw.2 q hq)

def pathCost (meet : S → S → S) (weight : G → S) (top : S) : List G → S
  | [] => top
  | g :: rest => meet (weight g) (pathCost meet weight top rest)

def paths (choices : Nat → Q → List G) (next : Nat → Q → G → Q)
    (terminal : Q → Bool) : Nat → Q → List (List G)
  | 0, state => if terminal state then [[]] else []
  | n+1, state => (choices n state).flatMap
      (fun g => (paths choices next terminal n (next n state g)).map (g :: ·))

def solve (le : S → S → Prop) [DecidableRel le]
    (meet : S → S → S) (weight : G → S) (top : S)
    (choices : Nat → Q → List G) (next : Nat → Q → G → Q)
    (terminal : Q → Bool) : Nat → Q → Option (List G)
  | 0, state => if terminal state then some [] else none
  | n+1, state => V19DP.best le (pathCost meet weight top)
      ((choices n state).flatMap (fun g =>
        (solve le meet weight top choices next terminal n (next n state g)).toList.map (g :: ·)))

theorem solve_correct (le : S → S → Prop) [DecidableRel le]
    (refl : ∀ a, le a a)
    (trans : ∀ a b c, le a b → le b c → le a c)
    (total : ∀ a b, le a b ∨ le b a)
    (meet : S → S → S) (weight : G → S) (top : S)
    (monotone : ∀ a b c, le b c → le (meet a b) (meet a c))
    (choices : Nat → Q → List G) (next : Nat → Q → G → Q)
    (terminal : Q → Bool) (n : Nat) (state : Q) :
    Correct le (pathCost meet weight top)
      (solve le meet weight top choices next terminal n state)
      (paths choices next terminal n state) := by
  induction n generalizing state with
  | zero =>
    cases h : terminal state
    · simp [solve, paths, h, Correct]
    · simp [solve, paths, h, Correct, refl]
  | succ n ih =>
    apply best_of_cover le refl trans total
    · intro path member
      obtain ⟨g,hg,hpath⟩ := List.mem_flatMap.mp member
      obtain ⟨tail,htail,equal⟩ := List.mem_map.mp hpath
      have selected : solve le meet weight top choices next terminal n (next n state g)=some tail :=
        by simpa using htail
      have legal := (ih (next n state g)).2 tail selected
      apply List.mem_flatMap.mpr
      refine ⟨g,hg,?_⟩
      exact List.mem_map.mpr ⟨tail,legal.1,equal⟩
    · intro path member
      obtain ⟨g,hg,hpath⟩ := List.mem_flatMap.mp member
      obtain ⟨tail,htail,equal⟩ := List.mem_map.mp hpath
      cases answer : solve le meet weight top choices next terminal n (next n state g) with
      | none =>
        have empty := (ih (next n state g)).1.mp answer
        simp [empty] at htail
      | some chosen =>
        have optimal := (ih (next n state g)).2 chosen answer
        refine ⟨g :: chosen, ?_, ?_⟩
        · apply List.mem_flatMap.mpr
          refine ⟨g,hg,?_⟩
          apply List.mem_map.mpr
          exact ⟨chosen,by simp [answer],rfl⟩
        · rw [← equal]
          exact monotone (weight g) (pathCost meet weight top tail)
            (pathCost meet weight top chosen) (optimal.2 tail htail)

theorem paths_length (choices : Nat → Q → List G) (next : Nat → Q → G → Q)
    (terminal : Q → Bool) (n : Nat) (state : Q) (path : List G)
    (legal : path ∈ paths choices next terminal n state) : path.length=n := by
  induction n generalizing state path with
  | zero =>
    cases h : terminal state <;> simp [paths,h] at legal
    subst path
    rfl
  | succ n ih =>
    obtain ⟨g,_,hpath⟩ := List.mem_flatMap.mp legal
    obtain ⟨tail,htail,rfl⟩ := List.mem_map.mp hpath
    simpa using congrArg Nat.succ (ih (next n state g) tail htail)

end V19Layer

#print axioms V19Layer.best_of_cover
#print axioms V19Layer.solve_correct
#print axioms V19Layer.paths_length
