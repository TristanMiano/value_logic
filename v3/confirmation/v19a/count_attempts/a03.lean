import Std

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
