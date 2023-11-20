open Bag
open Model

(** A model that can predict a sequence of words. *)
module type NgramType = sig
  (** Representation type. *)
  type t

  (** Given an integer [n] and a training corpus consisting of a list of words
      [lst], produce a Ngram model for n-grams. Requires: [n > 0]. *)
  val build : int -> string list -> t

  (** Given an integer [max_length] and a prompt consisting of a list of strings
      [prompt], generate up to [max_length] words. Requires: [max_length >= 0]. *)
  val sample_sequence : t -> int -> string list -> string list
end

(** Construct a Ngram model from a predict-the-next-word model. *)
module Ngram (Model : ModelType) : NgramType

(** A Ngram model that repeatedly predicts a random word. *)
module Rand_ngram : NgramType

(** A Ngram model that repeatedly predicts the most frequent next word. *)
module Freq_ngram : NgramType

(** A Ngram model that interpolates between two random Ngram models. *)
module Interp_ngram : NgramType

(** Sanitize a string by removing non-alphanumeric symbols. Return the
    list of words obtained by splitting on spaces. *)
val sanitize : string -> string list

(** Build a random Ngram model from a training corpus consisting of a
    list of words, and an integer parameter [n]. Requires: [n > 0]. *)
val build_rand_ngram : string -> int -> Rand_ngram.t

(** Build a most-frequent Ngram model from a training corpus consisting of a
    list of words, and an integer parameter [n]. Requires: [n > 0]. *)
val build_freq_ngram : string -> int -> Freq_ngram.t

(** Build an interpolated Ngram model from a training corpus consisting of a
    list of words, and an integer parameter [n]. Requires: [n > 1]. *)
val build_interp_ngram : string -> int -> Interp_ngram.t

(** Given a maximum number [N] of words to generate and a prompt consisting of a
    list of words, generate up to [N] words using the random Ngram model.
    Requires: [N >= 0]. *)
val create_rand_sequence : Rand_ngram.t -> int -> string -> string

(** Given a maximum number [N] of words to generate and a prompt consisting of a
    list of words, generate up to [N] words using the most-frequent Ngram model.
    Requires: [N >= 0]. *)
val create_freq_sequence : Freq_ngram.t -> int -> string -> string

(** Given a maximum number [N] of words to generate and a prompt consisting of a
    list of words, generate up to [N] words using the most-frequent Ngram model.
    Requires: [N >= 0]. *)
val create_interp_sequence : Interp_ngram.t -> int -> string -> string
