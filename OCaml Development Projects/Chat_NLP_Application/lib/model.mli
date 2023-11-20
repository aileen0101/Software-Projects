open Bag

(** A model can predict the next word. *)
module type ModelType = sig
  type t
  (** Representation type of the model. *)

  val build : int -> string list -> t
  (** Build a model, given an integer parameter [n] describing the size of
      n-grams and a list of strings [corpus]. Requires: [n > 0]. *)

  val generate_next : t -> string list -> string option
  (** Given a list of strings [prompt], generate the next word. Returns [None]
      if the model can't generate a word. Requires: the length of [prompt] must
      be at least [n - 1], where [n] is the n-gram size. *)

  val list_ngrams : t -> string list list
  (** Produce the list of n-grams that are stored in the model. No n-gram should
      be produced more than once. *)

  val size : t -> int
  (** Get the parameter [n], for a n-gram model. *)
end

val chunks : int -> 'a list -> 'a list list
(** Given a positive integer [n] and a list of items [l], produce a list of all
    contiguous sublists of length [n] of the input list. If [n] is bigger than
    [l], return the empty list. Requires: [n > 0]. *)

val split_last : 'a list -> 'a * 'a list
(** Given a nonempty list [l], returns a pair consisting of the last element and
    a list of all previous elements in their original order. This should take
    O(n) time. Requires: the input list [l] is nonempty. *)

module String_list_map : Map.S with type key = string list
(** A Map whose keys are lists of strings. *)

(** A model based on a sampleable bag [Bag]. *)
module BagModel (Bag : SampleBagType) : ModelType

(** A model that interpolates between two copies of the same model [Model], with
    different parameters [n]. *)
module InterpModel (Model : ModelType) : ModelType
