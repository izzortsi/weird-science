/-
  Mereotopological Ontology with Compositional Algebra
  A Self-Contained Formalization in Lean 4
  
  No Mathlib dependencies - all structures defined from first principles.
  
  Author: Igor Strozzi
  Course: Intuitionistic Type Theory and Lean (Prof. Francesco Noseda)
-/

universe u v

/-! ## Section 1: Algebraic Foundations -/

/-- A partial order with explicit axioms -/
class PartialOrder' (α : Type u) where
  le : α → α → Prop
  le_refl : ∀ a, le a a
  le_trans : ∀ {a b c}, le a b → le b c → le a c
  le_antisymm : ∀ {a b}, le a b → le b a → a = b

instance {α : Type u} [PartialOrder' α] : LE α := ⟨PartialOrder'.le⟩

/-- A lattice has meet and join operations -/
class Lattice' (α : Type u) extends PartialOrder' α where
  inf : α → α → α
  sup : α → α → α
  inf_le_left : ∀ a b, le (inf a b) a
  inf_le_right : ∀ a b, le (inf a b) b
  le_inf : ∀ {a b c}, le a b → le a c → le a (inf b c)
  le_sup_left : ∀ a b, le a (sup a b)
  le_sup_right : ∀ a b, le b (sup a b)
  sup_le : ∀ {a b c}, le a c → le b c → le (sup a b) c

namespace Lattice'
variable {α : Type u} [Lattice' α]

-- Useful derived properties
theorem inf_comm (a b : α) : inf a b = inf b a := by
  apply le_antisymm
  · exact le_inf (inf_le_right a b) (inf_le_left a b)
  · exact le_inf (inf_le_right b a) (inf_le_left b a)

theorem inf_assoc (a b c : α) : inf (inf a b) c = inf a (inf b c) := by
  apply le_antisymm
  · apply le_inf
    · exact le_trans (inf_le_left _ _) (inf_le_left _ _)
    · apply le_inf
      · exact le_trans (inf_le_left _ _) (inf_le_right _ _)
      · exact inf_le_right _ _
  · apply le_inf
    · apply le_inf
      · exact inf_le_left _ _
      · exact le_trans (inf_le_right _ _) (inf_le_left _ _)
    · exact le_trans (inf_le_right _ _) (inf_le_right _ _)

theorem inf_idem (a : α) : inf a a = a := by
  apply le_antisymm
  · exact inf_le_left a a
  · exact le_inf (le_refl a) (le_refl a)

theorem sup_comm (a b : α) : sup a b = sup b a := by
  apply le_antisymm
  · exact sup_le (le_sup_right b a) (le_sup_left b a)
  · exact sup_le (le_sup_right a b) (le_sup_left a b)

end Lattice'

/-- A bounded lattice has top and bottom elements -/
class BoundedLattice (α : Type u) extends Lattice' α where
  top : α
  bot : α
  le_top : ∀ a, le a top
  bot_le : ∀ a, le bot a

namespace BoundedLattice
variable {α : Type u} [BoundedLattice α]

notation "⊤" => top
notation "⊥" => bot

theorem inf_bot (a : α) : Lattice'.inf a bot = bot := by
  apply le_antisymm
  · exact Lattice'.inf_le_right a bot
  · exact bot_le _

theorem sup_top (a : α) : Lattice'.sup a top = top := by
  apply le_antisymm
  · exact le_top _
  · exact Lattice'.le_sup_right a top

end BoundedLattice

/-- A Heyting algebra: the algebraic semantics of intuitionistic logic -/
class HeytingAlgebra (α : Type u) extends BoundedLattice α where
  /-- Relative pseudo-complement (Heyting implication) -/
  himp : α → α → α
  /-- The defining adjunction: a ⊓ b ≤ c ↔ a ≤ b ⇨ c -/
  le_himp_iff : ∀ {a b c}, le (Lattice'.inf a b) c ↔ le a (himp b c)

namespace HeytingAlgebra
variable {α : Type u} [HeytingAlgebra α]

-- Notation for Heyting implication
infixr:60 " ⇨ " => himp

/-- Pseudo-complement (negation) -/
def hnot (a : α) : α := himp a bot
prefix:80 "∼" => hnot

-- Key theorems

/-- Modus ponens in the algebra -/
theorem himp_inf_le (a b : α) : Lattice'.inf a (a ⇨ b) ≤ b := by
  have h := le_himp_iff.mpr (le_refl (a ⇨ b))
  rw [Lattice'.inf_comm] at h
  exact h

/-- a ≤ b implies a ⇨ b = ⊤ -/
theorem himp_eq_top_of_le {a b : α} (h : a ≤ b) : (a ⇨ b) = top := by
  apply le_antisymm
  · exact le_top _
  · apply le_himp_iff.mp
    calc Lattice'.inf top a 
        = Lattice'.inf a top := Lattice'.inf_comm _ _
      _ = a := by apply le_antisymm; exact Lattice'.inf_le_left _ _; 
                  exact Lattice'.le_inf (le_refl _) (le_top _)
      _ ≤ b := h

/-- Reflexivity of implication -/
theorem himp_self (a : α) : (a ⇨ a) = top := himp_eq_top_of_le (le_refl a)

/-- Double negation introduction -/
theorem le_hnot_hnot (a : α) : a ≤ ∼(∼a) := by
  apply le_himp_iff.mp
  calc Lattice'.inf (∼a) a 
      = Lattice'.inf a (∼a) := Lattice'.inf_comm _ _
    _ = Lattice'.inf a (a ⇨ bot) := rfl
    _ ≤ bot := himp_inf_le a bot

end HeytingAlgebra


/-! ## Section 2: Mereotopological Ontology -/

/-- A mereotopological ontology: concepts with part-whole and connection -/
class MereotopologicalOntology (O : Type u) where
  /-- Parthood relation -/
  partOf : O → O → Prop
  /-- Connection relation -/
  C : O → O → Prop
  -- Mereological axioms
  partOf_refl : ∀ x, partOf x x
  partOf_trans : ∀ {x y z}, partOf x y → partOf y z → partOf x z
  partOf_antisymm : ∀ {x y}, partOf x y → partOf y x → x = y
  -- Topological axioms
  C_refl : ∀ x, C x x
  C_symm : ∀ {x y}, C x y → C y x
  -- Coherence
  part_connected : ∀ {x y}, partOf x y → C x y

namespace MereotopologicalOntology
variable {O : Type u} [MereotopologicalOntology O]

/-- Proper parthood -/
def PP (x y : O) : Prop := partOf x y ∧ x ≠ y

/-- Overlap -/
def Overlap (x y : O) : Prop := ∃ z, partOf z x ∧ partOf z y

/-- Disjointness -/
def Disjoint (x y : O) : Prop := ¬ Overlap x y

/-- External connection -/
def EC (x y : O) : Prop := C x y ∧ Disjoint x y

-- Basic theorems
theorem Overlap_refl (x : O) : Overlap x x := ⟨x, partOf_refl x, partOf_refl x⟩

theorem Overlap_symm {x y : O} (h : Overlap x y) : Overlap y x :=
  let ⟨z, hz1, hz2⟩ := h; ⟨z, hz2, hz1⟩

theorem partOf_implies_Overlap {x y : O} (h : partOf x y) : Overlap x y :=
  ⟨x, partOf_refl x, h⟩

end MereotopologicalOntology


/-! ## Section 3: Compositional Algebra -/

/-- A compositional algebra extends Heyting algebra with
    named operations for conceptual composition -/
class CompositionalAlgebra (A : Type v) extends HeytingAlgebra A where
  /-- Derivability relation -/
  derives : A → A → Prop := fun a b => Lattice'.inf a b = a

namespace CompositionalAlgebra
variable {A : Type v} [CompositionalAlgebra A]

open Lattice' HeytingAlgebra BoundedLattice

/-- Conceptual conjunction/composition -/
def compose (a b : A) : A := inf a b

/-- Sequential composition (implication) -/
def seq (a b : A) : A := himp a b

/-- Conceptual disjunction -/
def choice (a b : A) : A := sup a b

notation:70 a " ⊗ " b => compose a b
notation:60 a " ⟹ " b => seq a b
notation:65 a " ⊕ " b => choice a b

-- Composition properties
theorem compose_comm (a b : A) : a ⊗ b = b ⊗ a := inf_comm a b

theorem compose_assoc (a b c : A) : (a ⊗ b) ⊗ c = a ⊗ (b ⊗ c) := inf_assoc a b c

theorem compose_idem (a : A) : a ⊗ a = a := inf_idem a

/-- The adjunction captures the deductive nature -/
theorem adjunction (a b c : A) : (a ⊗ b) ≤ c ↔ a ≤ (b ⟹ c) := le_himp_iff

end CompositionalAlgebra


/-! ## Section 4: Ontological Algebra - The Action -/

/-- An ontological algebra: the algebra 𝒜 acting on ontology 𝒪 -/
class OntologicalAlgebra (O : Type u) (A : Type v)
    [MereotopologicalOntology O] [CompositionalAlgebra A] where
  /-- Interpretation function -/
  interp : O → A
  /-- Preserves mereological structure -/
  interp_mono : ∀ {c₁ c₂ : O}, MereotopologicalOntology.partOf c₁ c₂ → 
    interp c₁ ≤ interp c₂
  /-- Connected concepts have non-trivial composition -/
  connected_nontrivial : ∀ {c₁ c₂ : O}, MereotopologicalOntology.C c₁ c₂ → 
    Lattice'.inf (interp c₁) (interp c₂) ≠ BoundedLattice.bot

namespace OntologicalAlgebra
variable {O : Type u} {A : Type v}
variable [MereotopologicalOntology O] [CompositionalAlgebra A]
variable [OntologicalAlgebra O A]

open Lattice' HeytingAlgebra BoundedLattice CompositionalAlgebra

/-- Semantic brackets -/
notation "⦃" c "⦄" => interp c

/-- The fundamental operation: (C₁, C₂) ↦ ⦃C₁⦄ ⊓ ⦃C₂⦄ ∈ A -/
def combine (c₁ c₂ : O) : A := ⦃c₁⦄ ⊗ ⦃c₂⦄

/-- Conceptual implication -/
def conceptImpl (c₁ c₂ : O) : A := ⦃c₁⦄ ⟹ ⦃c₂⦄

notation c₁ " ▷ " c₂ => combine c₁ c₂
notation c₁ " ⊸ " c₂ => conceptImpl c₁ c₂

-- Key theorems

/-- Parthood induces algebraic derivability -/
theorem partOf_derives {c₁ c₂ : O}
    (h : MereotopologicalOntology.partOf c₁ c₂) :
    ⦃c₁⦄ ⊗ ⦃c₂⦄ = ⦃c₁⦄ := by
  apply le_antisymm
  · exact inf_le_left ⦃c₁⦄ ⦃c₂⦄
  · exact le_inf (le_refl ⦃c₁⦄) (interp_mono h)

/-- Overlapping concepts have non-trivial combination -/
theorem overlap_nontrivial {c₁ c₂ : O}
    (h : MereotopologicalOntology.Overlap c₁ c₂) :
    (c₁ ▷ c₂) ≠ bot := by
  obtain ⟨z, hz1, hz2⟩ := h
  intro hcontra
  have h1 : ⦃z⦄ ≤ ⦃c₁⦄ := interp_mono hz1
  have h2 : ⦃z⦄ ≤ ⦃c₂⦄ := interp_mono hz2
  have h3 : ⦃z⦄ ≤ (c₁ ▷ c₂) := le_inf h1 h2
  have h4 : ⦃z⦄ ≤ bot := by rw [← hcontra]; exact h3
  have hconn := MereotopologicalOntology.C_refl z
  have hne := connected_nontrivial hconn
  rw [inf_idem] at hne
  have heq : ⦃z⦄ = bot := le_antisymm h4 (bot_le ⦃z⦄)
  exact hne heq

/-- Modus ponens for concepts -/
theorem concept_modus_ponens (c₁ c₂ : O) :
    ⦃c₁⦄ ⊗ (c₁ ⊸ c₂) ≤ ⦃c₂⦄ :=
  himp_inf_le ⦃c₁⦄ ⦃c₂⦄

/-- Parthood implies implication is top -/
theorem partOf_impl_top {c₁ c₂ : O}
    (h : MereotopologicalOntology.partOf c₁ c₂) :
    (c₁ ⊸ c₂) = top :=
  himp_eq_top_of_le (interp_mono h)

end OntologicalAlgebra


/-! ## Section 5: Concrete Example - Three-Element Chain -/

/-- A simple three-element Heyting algebra: ⊥ < a < ⊤ -/
inductive Three where
  | bot : Three
  | mid : Three
  | top : Three
  deriving DecidableEq, Repr

namespace Three

def le : Three → Three → Prop
  | bot, _ => True
  | mid, bot => False
  | mid, _ => True
  | top, top => True
  | top, _ => False

def inf : Three → Three → Three
  | bot, _ => bot
  | _, bot => bot
  | top, y => y
  | x, top => x
  | mid, mid => mid

def sup : Three → Three → Three
  | top, _ => top
  | _, top => top
  | bot, y => y
  | x, bot => x
  | mid, mid => mid

def himp : Three → Three → Three
  | _, top => top
  | bot, _ => top
  | top, bot => bot
  | top, mid => mid
  | mid, bot => bot
  | mid, mid => top

instance : PartialOrder' Three where
  le := le
  le_refl := fun a => by cases a <;> simp [le]
  le_trans := fun {a b c} hab hbc => by
    cases a <;> cases b <;> cases c <;> simp_all [le]
  le_antisymm := fun {a b} hab hba => by
    cases a <;> cases b <;> simp_all [le]

instance : Lattice' Three where
  inf := inf
  sup := sup
  inf_le_left := fun a b => by cases a <;> cases b <;> simp [inf, le]
  inf_le_right := fun a b => by cases a <;> cases b <;> simp [inf, le]
  le_inf := fun {a b c} hab hac => by
    cases a <;> cases b <;> cases c <;> simp_all [inf, le]
  le_sup_left := fun a b => by cases a <;> cases b <;> simp [sup, le]
  le_sup_right := fun a b => by cases a <;> cases b <;> simp [sup, le]
  sup_le := fun {a b c} hac hbc => by
    cases a <;> cases b <;> cases c <;> simp_all [sup, le]

instance : BoundedLattice Three where
  top := Three.top
  bot := Three.bot
  le_top := fun a => by cases a <;> simp [le]
  bot_le := fun a => by simp [le]

instance : HeytingAlgebra Three where
  himp := himp
  le_himp_iff := fun {a b c} => by
    cases a <;> cases b <;> cases c <;> simp [inf, himp, le]

instance : CompositionalAlgebra Three where

end Three


/-! ## Section 6: A Simple Ontology Example -/

/-- A simple three-concept ontology -/
inductive SimpleConcepts where
  | nothing : SimpleConcepts   -- Universal bottom
  | entity : SimpleConcepts    -- Generic entity  
  | everything : SimpleConcepts -- Universal top
  deriving DecidableEq, Repr

namespace SimpleConcepts

def partOf : SimpleConcepts → SimpleConcepts → Prop
  | nothing, _ => True
  | entity, nothing => False
  | entity, _ => True  
  | everything, everything => True
  | everything, _ => False

def C : SimpleConcepts → SimpleConcepts → Prop
  | nothing, nothing => True
  | nothing, _ => False
  | _, nothing => False
  | _, _ => True

instance : MereotopologicalOntology SimpleConcepts where
  partOf := partOf
  C := C
  partOf_refl := fun x => by cases x <;> simp [partOf]
  partOf_trans := fun {x y z} hxy hyz => by
    cases x <;> cases y <;> cases z <;> simp_all [partOf]
  partOf_antisymm := fun {x y} hxy hyx => by
    cases x <;> cases y <;> simp_all [partOf]
  C_refl := fun x => by cases x <;> simp [C]
  C_symm := fun {x y} h => by cases x <;> cases y <;> simp_all [C]
  part_connected := fun {x y} h => by
    cases x <;> cases y <;> simp_all [partOf, C]

/-- The interpretation into Three -/
def interpSimple : SimpleConcepts → Three
  | nothing => Three.bot
  | entity => Three.mid
  | everything => Three.top

instance : OntologicalAlgebra SimpleConcepts Three where
  interp := interpSimple
  interp_mono := fun {c₁ c₂} h => by
    cases c₁ <;> cases c₂ <;> simp_all [interpSimple, partOf, Three.le]
  connected_nontrivial := fun {c₁ c₂} h => by
    cases c₁ <;> cases c₂ <;> simp_all [C, interpSimple, Three.inf]

-- Example computations
#eval interpSimple SimpleConcepts.entity  -- Three.mid
#eval Three.inf (interpSimple SimpleConcepts.entity) 
                (interpSimple SimpleConcepts.everything)  -- Three.mid

end SimpleConcepts
