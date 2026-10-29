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


set_option autoImplicit false

namespace V19Count

universe u v
variable {A : Type u} {B : Type v}

def words (alphabet : List A) : (k : Nat) → List (Fin k → A)
  | 0 => [fun j => Fin.elim0 j]
  | k+1 => alphabet.flatMap (fun a => (words alphabet k).map (fun f => Fin.cases a f))

theorem flatMap_length_const (alphabet : List A) (f : A → List B) (size : Nat)
    (fixed : ∀ a, a ∈ alphabet → (f a).length=size) :
    (alphabet.flatMap f).length=alphabet.length*size := by
  induction alphabet with
  | nil => simp
  | cons a rest ih =>
    simp only [List.flatMap_cons, List.length_append]
    rw [fixed a (by simp), ih (fun b hb => fixed b (List.mem_cons_of_mem a hb))]
    simp [Nat.succ_mul, Nat.add_comm]

theorem words_length (alphabet : List A) (k : Nat) :
    (words alphabet k).length=alphabet.length^k := by
  induction k with
  | zero => simp [words]
  | succ k ih =>
    rw [words, flatMap_length_const alphabet
      (fun a => (words alphabet k).map (fun f =>
        (fun j => Fin.cases (motive := fun _ => A) a f j : Fin (k+1) → A)))
      (words alphabet k).length (by intro a _; simp)]
    rw [ih]
    simp [Nat.pow_succ, Nat.mul_comm]

theorem words_complete (alphabet : List A) (k : Nat) (f : Fin k → A)
    (values : ∀ j, f j ∈ alphabet) : f ∈ words alphabet k := by
  induction k with
  | zero =>
    have same : f=(fun j => Fin.elim0 j) := by
      funext j
      exact Fin.elim0 j
    simp [words, same]
  | succ k ih =>
    apply List.mem_flatMap.mpr
    refine ⟨f 0, values 0, ?_⟩
    apply List.mem_map.mpr
    refine ⟨(fun j => f j.succ), ih (fun j => f j.succ) (fun j => values j.succ), ?_⟩
    funext j
    exact Fin.cases rfl (fun _ => rfl) j

def binaryMasks (k : Nat) : List (Fin k → Bool) := words [false,true] k

theorem binaryMasks_length (k : Nat) : (binaryMasks k).length=2^k := by
  simpa [binaryMasks] using words_length [false,true] k

theorem binaryMasks_complete (k : Nat) (mask : Fin k → Bool) :
    mask ∈ binaryMasks k := by
  apply words_complete
  intro j
  cases mask j <;> simp

theorem assignments_length (n k : Nat) :
    (words (List.finRange n) k).length=n^k := by
  simpa using words_length (List.finRange n) k

theorem assignments_complete (n k : Nat) (assignment : Fin k → Fin n) :
    assignment ∈ words (List.finRange n) k := by
  apply words_complete
  intro j
  simp

inductive State where
  | outside
  | remainder
  | assigned
  deriving DecidableEq

def stateS : State → Bool
  | .outside => false
  | .remainder => true
  | .assigned => true

def stateT : State → Bool
  | .outside => false
  | .remainder => false
  | .assigned => true

def encode (s t : Bool) : State :=
  if s then if t then .assigned else .remainder else .outside

theorem encode_decode (s t : Bool) (nested : t=true → s=true) :
    stateS (encode s t)=s ∧ stateT (encode s t)=t := by
  cases s <;> cases t <;> simp_all [encode, stateS, stateT]

def nestedPairs (k : Nat) : List ((Fin k → Bool) × (Fin k → Bool)) :=
  (words [State.outside,State.remainder,State.assigned] k).map
    (fun word => ((fun j => stateS (word j)), (fun j => stateT (word j))))

theorem nestedPairs_length (k : Nat) : (nestedPairs k).length=3^k := by
  simp only [nestedPairs, List.length_map]
  simpa using words_length [State.outside,State.remainder,State.assigned] k

theorem nestedPairs_sound (k : Nat) (s t : Fin k → Bool)
    (member : (s,t) ∈ nestedPairs k) : ∀ j, t j=true → s j=true := by
  obtain ⟨word, _, equal⟩ := List.mem_map.mp member
  cases equal
  intro j selected
  cases h : word j <;> simp_all [stateS, stateT]

theorem nestedPairs_complete (k : Nat) (s t : Fin k → Bool)
    (nested : ∀ j, t j=true → s j=true) : (s,t) ∈ nestedPairs k := by
  apply List.mem_map.mpr
  let word : Fin k → State := fun j => encode (s j) (t j)
  refine ⟨word, words_complete _ k word ?_, ?_⟩
  · intro j
    cases word j <;> simp
  · have equalS : (fun j => stateS (word j))=s :=
      funext (fun j => (encode_decode (s j) (t j) (nested j)).1)
    have equalT : (fun j => stateT (word j))=t :=
      funext (fun j => (encode_decode (s j) (t j) (nested j)).2)
    exact Prod.ext equalS equalT

#print axioms words_length
#print axioms words_complete
#print axioms binaryMasks_length
#print axioms binaryMasks_complete
#print axioms assignments_length
#print axioms assignments_complete
#print axioms nestedPairs_length
#print axioms nestedPairs_sound
#print axioms nestedPairs_complete

end V19Count

namespace V19Mask

universe u
variable {k : Nat}
abbrev Mask (k : Nat) := Fin k → Bool
abbrev Edge (k : Nat) := Nat × Mask k

def Subset (t s : Mask k) : Prop := ∀ j, t j=true → s j=true
def Empty (s : Mask k) : Prop := ∀ j, s j=false
def difference (s t : Mask k) : Mask k := fun j => s j && !(t j)

noncomputable def choices (available : Nat → Mask k → Prop)
    (layer : Nat) (state : Mask k) : List (Edge k) := by
  classical
  exact ((V19Count.binaryMasks k).filter
    (fun t => decide (Subset t state ∧ available layer t))).map (fun t => (layer,t))

def next (_ : Nat) (state : Mask k) (edge : Edge k) : Mask k :=
  difference state edge.2

noncomputable def terminal (state : Mask k) : Bool := by
  classical
  exact decide (Empty state)

def Good (available : Nat → Mask k → Prop) : Nat → Mask k → List (Edge k) → Prop
  | 0, state, [] => Empty state
  | 0, _, _ :: _ => False
  | _+1, _, [] => False
  | n+1, state, (j,t) :: rest =>
      j=n ∧ Subset t state ∧ available n t ∧ Good available n (difference state t) rest

theorem mem_choices (available : Nat → Mask k → Prop) (layer j : Nat)
    (state t : Mask k) :
    (j,t) ∈ choices available layer state ↔ j=layer ∧ Subset t state ∧ available layer t := by
  classical
  simp only [choices, List.mem_map]
  constructor
  · rintro ⟨a,member,equal⟩
    have facts : Subset a state ∧ available layer a := by
      simpa only [List.mem_filter, decide_eq_true_eq, V19Count.binaryMasks_complete, true_and]
        using member
    have hj : layer=j := congrArg Prod.fst equal
    have ht : a=t := congrArg Prod.snd equal
    subst j
    subst t
    exact ⟨rfl,facts⟩
  · rintro ⟨rfl,facts⟩
    refine ⟨t,?_,rfl⟩
    simpa only [List.mem_filter, decide_eq_true_eq, V19Count.binaryMasks_complete, true_and]
      using facts

theorem paths_iff_good (available : Nat → Mask k → Prop) (n : Nat)
    (state : Mask k) (path : List (Edge k)) :
    path ∈ V19Layer.paths (choices available) next terminal n state ↔
      Good available n state path := by
  classical
  induction n generalizing state path with
  | zero =>
    cases path with
    | nil => simp [V19Layer.paths, terminal, Good]
    | cons head rest => simp [V19Layer.paths, terminal, Good]
  | succ n ih =>
    constructor
    · intro member
      obtain ⟨edge,chosen,member⟩ := List.mem_flatMap.mp member
      obtain ⟨rest,legal,equal⟩ := List.mem_map.mp member
      rw [← equal]
      rcases edge with ⟨j,t⟩
      have facts := (mem_choices available n j state t).mp chosen
      exact ⟨facts.1,facts.2.1,facts.2.2,(ih _ _).mp legal⟩
    · intro good
      cases path with
      | nil => simp [Good] at good
      | cons edge rest =>
        rcases edge with ⟨j,t⟩
        obtain ⟨layer,nested,availableT,tail⟩ := good
        apply List.mem_flatMap.mpr
        refine ⟨(j,t),(mem_choices available n j state t).mpr ⟨layer,nested,availableT⟩,?_⟩
        apply List.mem_map.mpr
        exact ⟨rest,(ih _ _).mpr tail,rfl⟩

def hits (j : Fin k) : List (Edge k) → Nat
  | [] => 0
  | edge :: rest => (if edge.2 j then 1 else 0)+hits j rest

theorem good_assigns_once (available : Nat → Mask k → Prop) (n : Nat)
    (state : Mask k) (path : List (Edge k))
    (good : Good available n state path) :
    ∀ j, hits j path=if state j then 1 else 0 := by
  induction n generalizing state path with
  | zero =>
    cases path with
    | nil =>
      intro j
      have empty := good j
      simp [hits,empty]
    | cons head rest => simp [Good] at good
  | succ n ih =>
    cases path with
    | nil => simp [Good] at good
    | cons edge rest =>
      rcases edge with ⟨layer,t⟩
      obtain ⟨_,nested,_,tail⟩ := good
      intro j
      have remaining := ih (difference state t) rest tail j
      have nestedj := nested j
      cases ht : t j <;> cases hs : state j <;>
        simp_all [hits,difference]

theorem all_receipts_once (available : Nat → Mask k → Prop) (n : Nat)
    (path : List (Edge k))
    (legal : path ∈ V19Layer.paths (choices available) next terminal n (fun _ => true)) :
    ∀ j, hits j path=1 := by
  have good := (paths_iff_good available n (fun _ => true) path).mp legal
  simpa using good_assigns_once available n (fun _ => true) path good

theorem solve_legal_optimal {S : Type u} (le : S → S → Prop) [DecidableRel le]
    (refl : ∀ a, le a a) (trans : ∀ a b c, le a b → le b c → le a c)
    (total : ∀ a b, le a b ∨ le b a)
    (meet : S → S → S) (weight : Edge k → S) (top : S)
    (monotone : ∀ a b c, le b c → le (meet a b) (meet a c))
    (available : Nat → Mask k → Prop) (n : Nat) (state : Mask k)
    (winner : List (Edge k))
    (selected : V19Layer.solve le meet weight top (choices available) next terminal n state=some winner) :
    Good available n state winner ∧
      ∀ candidate, Good available n state candidate →
        le (V19Layer.pathCost meet weight top candidate) (V19Layer.pathCost meet weight top winner) := by
  have result := (V19Layer.solve_correct le refl trans total meet weight top monotone
    (choices available) next terminal n state).2 winner selected
  exact ⟨(paths_iff_good available n state winner).mp result.1,
    fun candidate good => result.2 candidate ((paths_iff_good available n state candidate).mpr good)⟩

theorem solve_none_iff {S : Type u} (le : S → S → Prop) [DecidableRel le]
    (refl : ∀ a, le a a) (trans : ∀ a b c, le a b → le b c → le a c)
    (total : ∀ a b, le a b ∨ le b a)
    (meet : S → S → S) (weight : Edge k → S) (top : S)
    (monotone : ∀ a b c, le b c → le (meet a b) (meet a c))
    (available : Nat → Mask k → Prop) (n : Nat) (state : Mask k) :
    V19Layer.solve le meet weight top (choices available) next terminal n state=none ↔
      ¬ ∃ path, Good available n state path := by
  rw [(V19Layer.solve_correct le refl trans total meet weight top monotone
    (choices available) next terminal n state).1]
  rw [List.eq_nil_iff_forall_not_mem]
  simp only [paths_iff_good, not_exists]

end V19Mask

#print axioms V19Mask.mem_choices
#print axioms V19Mask.paths_iff_good
#print axioms V19Mask.good_assigns_once
#print axioms V19Mask.all_receipts_once
#print axioms V19Mask.solve_legal_optimal
#print axioms V19Mask.solve_none_iff

namespace V19Mask

variable {k : Nat}

def Labels (available : Nat → Mask k → Prop) : Nat → List (Edge k) → Prop
  | 0, [] => True
  | 0, _ :: _ => False
  | _+1, [] => False
  | n+1, (j,t) :: rest => j=n ∧ available n t ∧ Labels available n rest

theorem good_iff_labels_counts (available : Nat → Mask k → Prop) (n : Nat)
    (state : Mask k) (path : List (Edge k)) :
    Good available n state path ↔ Labels available n path ∧
      ∀ j, hits j path=if state j then 1 else 0 := by
  induction n generalizing state path with
  | zero =>
    cases path with
    | nil =>
      constructor
      · intro good
        exact ⟨True.intro,good_assigns_once available 0 state [] good⟩
      · rintro ⟨_,counts⟩
        intro j
        have count := counts j
        cases hs : state j <;> simp_all [hits]
    | cons head rest => simp [Good,Labels]
  | succ n ih =>
    cases path with
    | nil => simp [Good,Labels]
    | cons edge rest =>
      rcases edge with ⟨layer,t⟩
      constructor
      · intro good
        have counts := good_assigns_once available (n+1) state ((layer,t)::rest) good
        obtain ⟨same,_,allowed,tail⟩ := good
        exact ⟨⟨same,allowed,((ih _ _).mp tail).1⟩,
          counts⟩
      · rintro ⟨labels,counts⟩
        obtain ⟨same,allowed,tailLabels⟩ := labels
        have nested : Subset t state := by
          intro j selected
          have count := counts j
          cases hs : state j <;> simp_all [hits]
        have tailCounts : ∀ j, hits j rest=if difference state t j then 1 else 0 := by
          intro j
          have count := counts j
          have contained := nested j
          cases ht : t j <;> cases hs : state j <;>
            simp_all [hits,difference]
        exact ⟨same,nested,allowed,(ih _ _).mpr ⟨tailLabels,tailCounts⟩⟩

theorem paths_iff_exact_partition (available : Nat → Mask k → Prop) (n : Nat)
    (state : Mask k) (path : List (Edge k)) :
    path ∈ V19Layer.paths (choices available) next terminal n state ↔
      Labels available n path ∧ ∀ j, hits j path=if state j then 1 else 0 := by
  exact (paths_iff_good available n state path).trans
    (good_iff_labels_counts available n state path)

end V19Mask

#print axioms V19Mask.good_iff_labels_counts
#print axioms V19Mask.paths_iff_exact_partition
