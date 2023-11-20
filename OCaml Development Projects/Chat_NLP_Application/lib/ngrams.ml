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
module Ngram (Model : ModelType) : NgramType = struct
  type t = Model.t

  (** Given an integer [n] and a training corpus consisting of a list of strings
      [input], produce a Ngram model for n-grams. Requires: [n > 0]. *)
  let build (n : int) (input : string list) : t = Model.build n input


  (** Given an integer [max_length] and a prompt consisting of a list of strings
      [prompt], generate up to [max_length] words. Requires: [max_length >= 0]. *)
  let rec sample_sequence (dist : Model.t) (max_length : int) (prompt : string list)
      : string list =
        if max_length = 0 then [] else
          match prompt with
            | [] -> []
            | h::t -> let next = Model.generate_next dist prompt in 
         match next with
            | None -> []
            | Some s -> s:: sample_sequence dist (max_length-1) (t@[s])
end
(* of module Ngram *)

(** A model that predicts the next word randomly. *)
module Rand_model = BagModel (RandomBag)

(** A model that predicts the most frequent next word. *)
module Freq_model = BagModel (FrequencyBag)

(** A Ngram model that repeatedly predicts the most frequent next word. *)
module Rand_ngram = Ngram (Rand_model)

(** A Ngram model that repeatedly predicts a random word. *)
module Freq_ngram = Ngram (Freq_model)

(** A Ngram model that interpolates between two random Ngram models. *)
module Interp_ngram = Ngram (InterpModel (Rand_model))

(** Sanitize a string by removing non-alphanumeric symbols. Return the
    list of words obtained by splitting on spaces. *)
let sanitize (s : string) : string list =
  s
  |> Str.global_replace (Str.regexp "[ \t\r\n]") " "
  |> Str.global_replace (Str.regexp "[^a-zA-Z0-9' ]") ""
  |> String.lowercase_ascii |> String.split_on_char ' '
  |> List.filter (fun s -> s <> "")

(** Build a random Ngram model from a training corpus consisting of a string
    [input] and an integer parameter [n]. Requires: [n > 0]. *)
let build_rand_ngram (input : string) (ngram_len : int) : Rand_ngram.t =
  input |> sanitize |> Rand_ngram.build ngram_len

(** Build a most-frequent Ngram model from a training corpus consisting of a
    string [input] and an integer parameter [n]. Requires: [n > 0]. *)
let build_freq_ngram (input : string) (ngram_len : int) : Freq_ngram.t =
  input |> sanitize |> Freq_ngram.build ngram_len

(** Build an interpolated Ngram model from a training corpus consisting of a
    string [input] and an integer parameter [n]. Requires: [n > 0]. *)
let build_interp_ngram (input : string) (ngram_len : int) : Interp_ngram.t
    =
  input |> sanitize |> Interp_ngram.build ngram_len

(** Given a maximum number [N] of words to generate and a prompt, generate up to
    [N] words using a random Ngram model. Requires: [N >= 0]. *)
let create_rand_sequence (dist : Rand_ngram.t) (max_len : int)
    (prompt : string) : string =
  prompt
  |> sanitize
  |> Rand_ngram.sample_sequence dist max_len
  |> String.concat " "

(** Given a maximum number [N] of words to generate and a prompt, generate up to
    [N] words using a most-frequent Ngram model. Requires: [N >= 0]. *)
let create_freq_sequence (dist : Freq_ngram.t) (max_len : int)
    (prompt : string) : string =
  prompt
  |> sanitize
  |> Freq_ngram.sample_sequence dist max_len
  |> String.concat " "

(** Given a maximum number [N] of words to generate and a prompt, generate up to
    [N] words using an interpolated Ngram model. Requires: [N >= 0]. *)
let create_interp_sequence (dist : Interp_ngram.t) (max_len : int)
    (prompt : string) : string =
  prompt
  |> sanitize
  |> Interp_ngram.sample_sequence dist max_len
  |> String.concat " "
